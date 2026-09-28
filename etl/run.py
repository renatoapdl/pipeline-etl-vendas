"""Executa o pipeline inteiro: CSV -> Parquet bruto -> limpeza e transformacao -> Parquet.

Uso:
    python etl/run.py
    python etl/run.py --entrada dados/vendas_bruto.csv --saida data
    spark-submit etl/run.py --entrada dados/vendas_bruto.csv
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from pyspark.sql.functions import col

from etl import extract, load, transform  # noqa: E402

ENTRADA_PADRAO = RAIZ / "dados" / "vendas_bruto.csv"
SAIDA_PADRAO = RAIZ / "data"


def get_spark(app_name: str = "etl-vendas"):
    """Sessao Spark local.

    O master so e definido quando o processo NAO veio do spark-submit. Se fosse definido
    sempre, o .master() sobrescreveria o --master da linha de comando e o job rodaria
    local mesmo num cluster.
    """
    from pyspark.sql import SparkSession

    builder = SparkSession.builder.appName(app_name).config(
        "spark.sql.session.timeZone", "America/Fortaleza"
    )
    if "PYSPARK_GATEWAY_PORT" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()


def main() -> None:
    parser = argparse.ArgumentParser(description="ETL de vendas: CSV -> Parquet -> Parquet tratado")
    parser.add_argument("--entrada", type=Path, default=ENTRADA_PADRAO, help="CSV de entrada")
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO, help="Pasta de saida")
    args = parser.parse_args()

    spark = get_spark()
    try:
        bruto = extract.ler_vendas(spark, args.entrada)
        total = bruto.count()
        print(f"\n[1] extraido: {total} linhas de {args.entrada.name}")
        print(f"    colunas: {', '.join(bruto.columns)}\n")

        destino_bruto = load.gravar_parquet(bruto, args.saida / "bruto" / "vendas")
        print(f"[2] bruto gravado em {destino_bruto.relative_to(RAIZ)}\n")

        # Cada regra e aplicada e contada separadamente, para dar para conferir o efeito
        # de cada uma no log em vez de so ver o resultado final.
        etapas = (
            ("R1 descartadas sem id ou data", transform.descartar_incompletos),
            ("R2 datas convertidas", transform.padronizar_datas),
            ("R3 valores convertidos", transform.converter_valores),
            ("R4 texto normalizado", transform.normalizar_texto),
            ("R5 nulos preenchidos", transform.preencher_nulos),
            ("R6 duplicadas removidas", transform.remover_duplicadas),
            ("D1 valor total criado", transform.criar_valor_total),
        )
        atual = bruto
        for nome, funcao in etapas:
            antes = atual.count()
            atual = funcao(atual)
            print(f"    {nome:32} {antes:>3} -> {atual.count():>3}")

        invalidas = atual.filter("data_venda is null").count()
        print(f"\n[3] tratada: {atual.count()} linhas" + (f", {invalidas} com data invalida" if invalidas else ""))

        # Nem todo nulo deve ser preenchido: uma venda sem preco continua nula, porque
        # inventar 0 ou 1 distorceria o faturamento. O pipeline so avisa e deixa a decisao
        # de negocio (descartar, corrigir na origem ou aprovar assim) para quem le.
        sem_preco = atual.filter(col("valor_unitario").isNull()).count()
        if sem_preco:
            print(f"    ATENCAO: {sem_preco} venda(s) sem valor_unitario; valor_total fica nulo")

        destino_tratado = load.gravar_parquet(atual, args.saida / "tratado" / "vendas")
        print(f"[4] tratado gravado em {destino_tratado.relative_to(RAIZ)}\n")

        print("[5] amostra do resultado:")
        atual.show(5, truncate=False)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
