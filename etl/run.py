"""Executa o pipeline Olist (Medallion: Bronze -> Silver -> Quality -> Gold)."""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from etl import bronze, gold, quality, silver  # noqa: E402
from etl.session import get_spark  # noqa: E402


def _imprimir(relatorio: quality.Relatorio) -> None:
    for linha in relatorio.linhas():
        print(f"    {linha}")


def main() -> None:
    spark = get_spark()
    try:
        print("[1] BRONZE")
        bronze.processar(spark)

        print("\n[2] SILVER")
        tabelas_silver = silver.processar(spark)

        print("\n[3] QUALITY GATE - Silver")
        relatorio_silver = quality.verificar_silver(tabelas_silver)
        _imprimir(relatorio_silver)
        if relatorio_silver.tem_erros:
            raise SystemExit("\nQUALITY GATE: publicacao do Gold bloqueada (Silver)\n")

        print("\n[4] GOLD")
        tabelas_gold = gold.gerar_gold(spark)

        print("\n[5] QUALITY GATE - Gold")
        relatorio_gold = quality.verificar_gold(tabelas_gold, tabelas_silver)
        _imprimir(relatorio_gold)
        if relatorio_gold.tem_erros:
            raise SystemExit("\nQUALITY GATE: publicacao do Gold bloqueada (Gold)\n")

        print("\n[6] PUBLICAR GOLD")
        gold.gravar_gold(tabelas_gold, gold.GOLD)

        print("\nETL Olist concluido com sucesso")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
