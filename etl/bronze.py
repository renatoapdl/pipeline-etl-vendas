"""Lê cada CSV em 'dados/olist' exatamente como eles chegaram, sem corrigir nada.

Regra da camada: A correção acontece na transformação, e
assim dá para conferir o que foi limpo comparando os dois Parquet.

Schema não declarado. Colunas tipadas no Silver.
"""

import os
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from etl.load import gravar_parquet
from etl.sessao import get_spark


#Patch - caminhos (bronze)
RAIZ = Path(__file__).resolve().parents[1]
ORIGEM = RAIZ / "dados" / "olist"
DADOS = Path(os.environ.get("ETL_DATA_DIR", RAIZ / "data"))
DESTINO = DADOS / "bronze"
ARQUIVOS = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]


# Função de leitura
def ler_csv(spark: SparkSession, caminho: Path) -> DataFrame:
    """Lê o CSV todo como texto."""
    if not caminho.exists():
        raise SystemExit(f"CSV não encontrado: {caminho}")

    return (
        spark.read.option("header", True)
        .option("encoding", "UTF-8")
        .option("delimiter", ",")
        .option("inferSchema", "false")
        .option("multiLine", "true")
        .option("escape", '"')
        .csv(str(caminho))
    )


# Processa a camada Bronze (lê os CSVs e grava o Parquet)
def processar(spark: SparkSession) -> None:
    for nome in ARQUIVOS:
        caminho = ORIGEM / nome
        print(f"Lendo: {nome}")
        df = ler_csv(spark, caminho)
        total = df.count()
        destino = gravar_parquet(df, DESTINO / caminho.stem)
        print(f"{caminho.stem}: {total} linhas -> {destino}")


# Função principal
def main() -> None:
    spark = get_spark()
    try:
        processar(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()