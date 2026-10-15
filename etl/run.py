"""Executa o pipeline inteiro (Medallion: Bronze -> Silver -> Gold).
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from etl import extract, gold, load, transform  # noqa: E402

ENTRADA_PADRAO = RAIZ / "dados" / "vendas_bruto.csv"
SAIDA_PADRAO = RAIZ / "data"


def get_spark(app_name: str = "etl-vendas"):
    """Sessao Spark local."""
    from pyspark.sql import SparkSession

    builder = SparkSession.builder.appName(app_name).config(
        "spark.sql.session.timeZone", "America/Fortaleza"
    )
    if "PYSPARK_GATEWAY_PORT" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()


def main() -> None:
    parser = argparse.ArgumentParser(description="ETL de vendas (Medallion: Bronze -> Silver -> Gold)")
    parser.add_argument("--entrada", type=Path, default=ENTRADA_PADRAO, help="CSV de entrada")
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO, help="Pasta de saida")
    args = parser.parse_args()

    spark = get_spark()
    try:
        bruto = extract.ler_vendas(spark, args.entrada)
        total = bruto.count()
        print(f"\n[1] BRONZE - extraido: {total} linhas de {args.entrada.name}")
        print(f"    colunas: {', '.join(bruto.columns)}\n")

        destino_bruto = load.gravar_parquet(bruto, args.saida / "bronze" / "vendas")
        print(f"[2] BRONZE gravado em {destino_bruto.relative_to(RAIZ)}\n")

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
            print(f"[{etapas.index((nome, funcao)) + 3}] SILVER - {nome}: {antes:>3} -> {atual.count():>3}")

        invalidas = atual.filter("data_venda is null").count()
        if invalidas:
            print(f"    ATENCAO: {invalidas} venda(s) com data invalida")

        sem_preco = atual.filter("valor_unitario is null").count()
        if sem_preco:
            print(f"    ATENCAO: {sem_preco} venda(s) sem valor_unitario; valor_total fica nulo")

        destino_tratado = load.gravar_parquet(atual, args.saida / "silver" / "vendas")
        print(f"\nSILVER gravado em {destino_tratado.relative_to(RAIZ)}")
        print(f"    linhas finais: {atual.count()}\n")

        gold_paths = gold.gravar_gold(atual, args.saida / "gold")
        print("GOLD gravado:")
        for camada, caminho in gold_paths.items():
            print(f"     - {camada}: {caminho.relative_to(RAIZ)}")
        print("\nETL (Medallion) concluido com sucesso\n")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
