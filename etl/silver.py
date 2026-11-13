"""Silver Olist — limpeza e tipagem, mantendo grão original."""

import os
from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from etl.load import gravar_parquet
from etl.session import get_spark

RAIZ = Path(__file__).resolve().parents[1]
DADOS = Path(os.environ.get("ETL_DATA_DIR", RAIZ / "data"))
BRONZE = DADOS / "bronze"
SILVER = DADOS / "silver"


# Função de leitura
def ler_bronze(spark: SparkSession, nome: str) -> DataFrame:
    return spark.read.parquet(str(BRONZE / nome))


# Funções de transformação

# Função de tradução de nomes de categorias de produtos
def transformar_translation(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("product_category_name", F.lower(F.trim(F.col("product_category_name"))))
          .withColumn("categoria_en", 
              F.when(F.lower(F.trim(F.col("product_category_name_english"))) == "", None)
               .otherwise(F.lower(F.trim(F.col("product_category_name_english"))))
          )
          .drop("product_category_name_english")
          .dropDuplicates(["product_category_name"])
    )


# Função de transformação de produtos
def transformar_products(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("product_id", F.trim(F.col("product_id").cast("string")))
            .withColumn("product_category_name", F.lower(F.trim(F.col("product_category_name").cast("string"))))
            .withColumn("product_photos_qty", F.col("product_photos_qty").cast("integer"))
            .withColumn("product_weight_g", F.col("product_weight_g").cast("integer"))
            .withColumn("product_length_cm", F.col("product_length_cm").cast("integer"))
            .withColumn("product_height_cm", F.col("product_height_cm").cast("integer"))
            .withColumn("product_width_cm", F.col("product_width_cm").cast("integer"))
            .drop("product_name_lenght", "product_description_lenght")
            .withColumnRenamed("product_photos_qty", "fotos_qty")
            .withColumnRenamed("product_weight_g", "peso_g")
            .withColumnRenamed("product_length_cm", "comprimento_cm")
            .withColumnRenamed("product_height_cm", "altura_cm")
            .withColumnRenamed("product_width_cm", "largura_cm")
    )


# Função de transformação de clientes
def transformar_customers(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("customer_id", F.trim(F.col("customer_id").cast("string")))
            .withColumn("customer_unique_id", F.trim(F.col("customer_unique_id").cast("string")))
            .withColumn("customer_zip_code_prefix", F.trim(F.col("customer_zip_code_prefix").cast("string")))
            .withColumn("customer_city", F.lower(F.trim(F.col("customer_city").cast("string"))))
            .withColumn("customer_state", F.upper(F.trim(F.col("customer_state").cast("string"))))
    )


#função de transformação de vendedores
def transformar_sellers(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("seller_id", F.trim(F.col("seller_id").cast("string")))
            .withColumn("seller_zip_code_prefix", F.trim(F.col("seller_zip_code_prefix").cast("string")))
            .withColumn("seller_city", F.lower(F.trim(F.col("seller_city").cast("string"))))
            .withColumn("seller_state", F.upper(F.trim(F.col("seller_state").cast("string"))))
    )


# Função de transformação de pedidos
def transformar_orders(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("order_id", F.trim(F.col("order_id").cast("string")))
            .withColumn("customer_id", F.trim(F.col("customer_id").cast("string")))
            .withColumn("order_status", F.lower(F.trim(F.col("order_status").cast("string"))))
            .withColumn("order_purchase_timestamp", F.to_timestamp(F.col("order_purchase_timestamp"), "yyyy-MM-dd HH:mm:ss"))
            .withColumn("order_approved_at", F.to_timestamp(F.col("order_approved_at"), "yyyy-MM-dd HH:mm:ss"))
            .withColumn("order_delivered_carrier_date", F.to_timestamp(F.col("order_delivered_carrier_date"), "yyyy-MM-dd HH:mm:ss"))
            .withColumn("order_delivered_customer_date", F.to_timestamp(F.col("order_delivered_customer_date"), "yyyy-MM-dd HH:mm:ss"))
            .withColumn("order_estimated_delivery_date", F.to_timestamp(F.col("order_estimated_delivery_date"), "yyyy-MM-dd HH:mm:ss"))
    )


# Função de transformação de itens do pedido
def transformar_items(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("order_id", F.trim(F.col("order_id").cast("string")))
            .withColumn("order_item_id", F.trim(F.col("order_item_id").cast("string")))
            .withColumn("product_id", F.trim(F.col("product_id").cast("string")))
            .withColumn("seller_id", F.trim(F.col("seller_id").cast("string")))
            .withColumn("shipping_limit_date", F.to_timestamp(F.col("shipping_limit_date"), "yyyy-MM-dd HH:mm:ss"))
            .withColumn("price", F.col("price").cast("decimal(12,2)"))
            .withColumn("freight_value", F.col("freight_value").cast("decimal(12,2)"))
    )


# Função de transformação de pagamentos
def transformar_payments(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("order_id", F.trim(F.col("order_id").cast("string")))
            .withColumn("payment_sequential", F.col("payment_sequential").cast("integer"))
            .withColumn("payment_type", F.lower(F.trim(F.col("payment_type").cast("string"))))
            .withColumn("payment_installments", F.col("payment_installments").cast("integer"))
            .withColumn("payment_value", F.col("payment_value").cast("decimal(12,2)"))
    )


# Processa a camada Silver e devolve as tabelas transformadas
def processar(spark: SparkSession) -> dict[str, DataFrame]:
    etapas = [
        ("translation", "product_category_name_translation", transformar_translation),
        ("products", "olist_products_dataset", transformar_products),
        ("customers", "olist_customers_dataset", transformar_customers),
        ("sellers", "olist_sellers_dataset", transformar_sellers),
        ("orders", "olist_orders_dataset", transformar_orders),
        ("items", "olist_order_items_dataset", transformar_items),
        ("payments", "olist_order_payments_dataset", transformar_payments),
    ]

    tabelas: dict[str, DataFrame] = {}
    for nome, origem, funcao in etapas:
        df = ler_bronze(spark, origem)
        df_silver = funcao(df)
        gravar_parquet(df_silver, SILVER / nome)
        print(f"{nome} OK")
        tabelas[nome] = df_silver
    return tabelas


# Função principal
def main() -> None:
    spark = get_spark("etl-olist-silver")
    try:
        processar(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()