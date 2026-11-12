from datetime import datetime
from decimal import Decimal

from pyspark.sql import functions as F

from etl import gold

SCHEMA_ITENS = (
    "order_id string, order_item_id string, product_id string, seller_id string, "
    "price decimal(12,2), freight_value decimal(12,2)"
)


def _unica_linha(df):
    linhas = df.collect()
    assert len(linhas) == 1
    return linhas[0]


def _dims_minimas(spark):
    dim_cliente = spark.createDataFrame(
        [(1, "u1")], "cod_cliente int, customer_unique_id string"
    )
    dim_produto = spark.createDataFrame(
        [(10, "p1")], "cod_produto int, product_id string"
    )
    dim_vendedor = spark.createDataFrame(
        [(100, "s1")], "cod_vendedor int, seller_id string"
    )
    dim_data = spark.createDataFrame([(20170105,)], "cod_data int")
    return dim_cliente, dim_produto, dim_vendedor, dim_data


def test_dim_cliente_mantem_ultimo_endereco_por_unique_id(spark):
    customers = spark.createDataFrame(
        [
            ("c1", "u1", "cidade antiga", "SP", "1"),
            ("c2", "u1", "cidade nova", "SP", "2"),
        ],
        (
            "customer_id string, customer_unique_id string, customer_city string, "
            "customer_state string, customer_zip_code_prefix string"
        ),
    )
    orders = spark.createDataFrame(
        [
            ("o1", "c1", datetime(2017, 1, 1)),
            ("o2", "c2", datetime(2018, 1, 1)),
        ],
        "order_id string, customer_id string, order_purchase_timestamp timestamp",
    )

    resultado = gold.criar_dim_cliente(customers, orders)

    linha = _unica_linha(resultado)
    assert linha["customer_unique_id"] == "u1"
    assert linha["cidade"] == "cidade nova"
    assert linha["cep_prefixo"] == "2"
    assert linha["cod_cliente"] == 1


def test_dim_vendedor_deduplica(spark):
    sellers = spark.createDataFrame(
        [
            ("s1", "cidade", "SP", "1"),
            ("s1", "cidade", "SP", "1"),
            ("s2", "outra", "RJ", "2"),
        ],
        (
            "seller_id string, seller_city string, seller_state string, "
            "seller_zip_code_prefix string"
        ),
    )

    resultado = gold.criar_dim_vendedor(sellers)

    assert resultado.count() == 2
    assert sorted(r["seller_id"] for r in resultado.collect()) == ["s1", "s2"]


def test_dim_data_gera_calendario(spark):
    orders = spark.createDataFrame(
        [("o1", datetime(2017, 1, 1)), ("o2", datetime(2017, 1, 3))],
        "order_id string, order_purchase_timestamp timestamp",
    )

    resultado = gold.criar_dim_data(orders)

    assert resultado.count() == 3
    linha = resultado.where(F.col("cod_data") == 20170102).first()
    assert linha["ano"] == 2017
    assert linha["mes"] == 1
    assert linha["dia"] == 2
    assert linha["ano_mes"] == 201701
    assert linha["trimestre"] == 1


def test_fato_itens_grao_e_fks(spark):
    items = spark.createDataFrame(
        [("o1", "1", "p1", "s1", Decimal("10.00"), Decimal("2.00"))],
        SCHEMA_ITENS,
    )
    orders = spark.createDataFrame(
        [("o1", "c1", datetime(2017, 1, 5))],
        "order_id string, customer_id string, order_purchase_timestamp timestamp",
    )
    customers = spark.createDataFrame(
        [("c1", "u1")], "customer_id string, customer_unique_id string"
    )
    dim_cliente, dim_produto, dim_vendedor, dim_data = _dims_minimas(spark)

    resultado = gold.criar_fato_itens(
        items, orders, customers, dim_cliente, dim_produto, dim_vendedor, dim_data
    )

    linha = _unica_linha(resultado)
    assert linha["cod_cliente"] == 1
    assert linha["cod_produto"] == 10
    assert linha["cod_vendedor"] == 100
    assert linha["cod_data"] == 20170105
    assert linha["price"] == Decimal("10.00")
    assert linha["freight_value"] == Decimal("2.00")


def test_fato_itens_descarta_data_fora_do_calendario(spark):
    items = spark.createDataFrame(
        [
            ("o1", "1", "p1", "s1", Decimal("10.00"), Decimal("2.00")),
            ("o2", "1", "p1", "s1", Decimal("5.00"), Decimal("1.00")),
        ],
        SCHEMA_ITENS,
    )
    orders = spark.createDataFrame(
        [
            ("o1", "c1", datetime(2017, 1, 5)),
            ("o2", "c1", datetime(2017, 1, 6)),
        ],
        "order_id string, customer_id string, order_purchase_timestamp timestamp",
    )
    customers = spark.createDataFrame(
        [("c1", "u1")], "customer_id string, customer_unique_id string"
    )
    dim_cliente, dim_produto, dim_vendedor, dim_data = _dims_minimas(spark)

    resultado = gold.criar_fato_itens(
        items, orders, customers, dim_cliente, dim_produto, dim_vendedor, dim_data
    )

    assert [r["order_id"] for r in resultado.collect()] == ["o1"]


def test_fato_pagamentos_grao_e_fks(spark):
    payments = spark.createDataFrame(
        [("o1", 1, "credit_card", 2, Decimal("12.00"))],
        (
            "order_id string, payment_sequential int, payment_type string, "
            "payment_installments int, payment_value decimal(12,2)"
        ),
    )
    orders = spark.createDataFrame(
        [("o1", "c1", datetime(2017, 1, 5))],
        "order_id string, customer_id string, order_purchase_timestamp timestamp",
    )
    customers = spark.createDataFrame(
        [("c1", "u1")], "customer_id string, customer_unique_id string"
    )
    dim_cliente = spark.createDataFrame(
        [(1, "u1")], "cod_cliente int, customer_unique_id string"
    )
    dim_data = spark.createDataFrame([(20170105,)], "cod_data int")

    resultado = gold.criar_fato_pagamentos(
        payments, orders, customers, dim_cliente, dim_data
    )

    linha = _unica_linha(resultado)
    assert linha["cod_cliente"] == 1
    assert linha["cod_data"] == 20170105
    assert linha["payment_value"] == Decimal("12.00")
