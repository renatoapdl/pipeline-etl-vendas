"""Gold Olist — Modelo Estrela (Dimensões e Fatos)."""

import os
from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from etl.load import gravar_parquet
from etl.sessao import get_spark


#Path - caminhos 
RAIZ = Path(__file__).resolve().parents[1]
DADOS = Path(os.environ.get("ETL_DATA_DIR", RAIZ / "data"))
SILVER = DADOS / "silver"
GOLD = DADOS / "gold"


# Funções de leitura

# Leitura do Silver
def ler_silver(spark: SparkSession, nome: str) -> DataFrame:
    return spark.read.parquet(str(SILVER / nome))


# Funções de criação das dimensões

# Dimensão Cliente
def criar_dim_cliente(df_customers: DataFrame, df_orders: DataFrame) -> DataFrame:
    w_endereco = Window.partitionBy("customer_unique_id").orderBy(
        F.col("order_purchase_timestamp").desc(),
        F.col("customer_id").desc(),
    )
    return (
        df_customers.join(
            df_orders.select("customer_id", "order_purchase_timestamp"),
            "customer_id",
            "left",
        )
        .withColumn("rn", F.row_number().over(w_endereco))
        .where(F.col("rn") == 1)
        .select(
            F.row_number().over(Window.orderBy("customer_unique_id")).alias("cod_cliente"),
            F.col("customer_unique_id"),
            F.col("customer_city").alias("cidade"),
            F.col("customer_state").alias("estado"),
            F.col("customer_zip_code_prefix").alias("cep_prefixo"),
        )
    )


# Dimensão Vendedor
def criar_dim_vendedor(df_sellers: DataFrame) -> DataFrame:
    return (
        df_sellers.dropDuplicates(["seller_id"])
        .select(
            F.row_number().over(Window.orderBy("seller_id")).alias("cod_vendedor"),
            F.col("seller_id"),
            F.col("seller_city").alias("cidade"),
            F.col("seller_state").alias("estado"),
            F.col("seller_zip_code_prefix").alias("cep_prefixo"),
        )
    )


# Dimensão Produto
def criar_dim_produto(df_products: DataFrame, df_translation: DataFrame) -> DataFrame:
    return (
        df_products.join(
            df_translation.select("product_category_name", "categoria_en"),
            "product_category_name",
            "left",
        )
        .select(
            F.row_number().over(Window.orderBy("product_id")).alias("cod_produto"),
            F.col("product_id"),
            F.col("product_category_name").alias("categoria_pt"),
            F.col("categoria_en"),
            F.col("peso_g"),
            F.col("comprimento_cm"),
            F.col("altura_cm"),
            F.col("largura_cm"),
            F.col("fotos_qty"),
        )
    )


# Dimensão Data
def criar_dim_data(df_orders: DataFrame) -> DataFrame:
    limites = df_orders.agg(
        F.min(F.to_date("order_purchase_timestamp")).alias("inicio"),
        F.max(F.to_date("order_purchase_timestamp")).alias("fim"),
    )
    calendario = limites.select(
        F.explode(
            F.sequence(F.col("inicio"), F.col("fim"), F.expr("interval 1 day"))
        ).alias("data")
    )
    return calendario.select(
        F.date_format("data", "yyyyMMdd").cast("integer").alias("cod_data"),
        F.col("data"),
        F.year("data").alias("ano"),
        F.month("data").alias("mes"),
        F.dayofmonth("data").alias("dia"),
        F.quarter("data").alias("trimestre"),
        (F.weekday("data") + 1).alias("dia_semana"),
        (F.weekday("data") >= 5).alias("eh_fim_de_semana"),
        F.date_format("data", "yyyyMM").cast("integer").alias("ano_mes"),
    )


# Funções de criação dos fatos

# Fato Itens
def criar_fato_itens(
    df_items: DataFrame,
    df_orders: DataFrame,
    df_customers: DataFrame,
    dim_cliente: DataFrame,
    dim_produto: DataFrame,
    dim_vendedor: DataFrame,
    dim_data: DataFrame,
) -> DataFrame:
    return (
        df_items
        .join(df_orders.select("order_id", "customer_id", "order_purchase_timestamp"), "order_id", "left")
        .join(df_customers.select("customer_id", "customer_unique_id"), "customer_id", "left")
        .join(dim_cliente.select("customer_unique_id", "cod_cliente"), "customer_unique_id", "left")
        .join(dim_produto.select("product_id", "cod_produto"), "product_id", "left")
        .join(dim_vendedor.select("seller_id", "cod_vendedor"), "seller_id", "left")
        .withColumn("cod_data", F.date_format("order_purchase_timestamp", "yyyyMMdd").cast("integer"))
        .join(dim_data.select("cod_data"), "cod_data", "inner")
        .select(
            "order_id", "order_item_id", "cod_cliente", "cod_produto",
            "cod_vendedor", "cod_data", "price", "freight_value",
        )
    )


# Fato Pagamentos
def criar_fato_pagamentos(
    df_payments: DataFrame,
    df_orders: DataFrame,
    df_customers: DataFrame,
    dim_cliente: DataFrame,
    dim_data: DataFrame,
) -> DataFrame:
    return (
        df_payments
        .join(df_orders.select("order_id", "customer_id", "order_purchase_timestamp"), "order_id", "left")
        .join(df_customers.select("customer_id", "customer_unique_id"), "customer_id", "left")
        .join(dim_cliente.select("customer_unique_id", "cod_cliente"), "customer_unique_id", "left")
        .withColumn("cod_data", F.date_format("order_purchase_timestamp", "yyyyMMdd").cast("integer"))
        .join(dim_data.select("cod_data"), "cod_data", "inner")
        .select(
            "order_id", "payment_sequential", "cod_cliente", "cod_data",
            "payment_type", "payment_installments", "payment_value",
        )
    )


# Gera todas as tabelas do Gold em memória (dimensões e fatos)
def gerar_gold(spark: SparkSession) -> dict[str, DataFrame]:
    df_customers = ler_silver(spark, "customers")
    df_orders = ler_silver(spark, "orders")
    df_sellers = ler_silver(spark, "sellers")
    df_products = ler_silver(spark, "products")
    df_translation = ler_silver(spark, "translation")
    df_items = ler_silver(spark, "items")
    df_payments = ler_silver(spark, "payments")

    dim_cliente = criar_dim_cliente(df_customers, df_orders)
    dim_vendedor = criar_dim_vendedor(df_sellers)
    dim_produto = criar_dim_produto(df_products, df_translation)
    dim_data = criar_dim_data(df_orders)

    fato_itens = criar_fato_itens(
        df_items, df_orders, df_customers, dim_cliente, dim_produto, dim_vendedor, dim_data
    )
    fato_pagamentos = criar_fato_pagamentos(
        df_payments, df_orders, df_customers, dim_cliente, dim_data
    )

    tabelas = {
        "dim_cliente": dim_cliente,
        "dim_vendedor": dim_vendedor,
        "dim_produto": dim_produto,
        "dim_data": dim_data,
        "fato_itens": fato_itens,
        "fato_pagamentos": fato_pagamentos,
    }
    for df in tabelas.values():
        df.cache()
    return tabelas


# Grava as tabelas do Gold em Parquet
def gravar_gold(tabelas: dict[str, DataFrame], destino: Path) -> dict[str, Path]:
    caminhos: dict[str, Path] = {}
    for nome, df in tabelas.items():
        caminhos[nome] = gravar_parquet(df, destino / nome)
        print(f"{nome} gravado em: {caminhos[nome]}")
    return caminhos


# Função principal - Gera e grava as dimensões e os fatos do Gold
def main() -> None:
    spark = get_spark()
    try:
        tabelas = gerar_gold(spark)
        gravar_gold(tabelas, GOLD)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()