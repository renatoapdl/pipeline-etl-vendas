from datetime import datetime
from decimal import Decimal

from etl import silver


def _unica_linha(df):
    linhas = df.collect()
    assert len(linhas) == 1
    return linhas[0]


def test_translation_normaliza_deduplica_e_traduz(spark):
    df = spark.createDataFrame(
        [
            (" Moveis ", " Furniture "),
            ("moveis", "FURNITURE"),
            ("", ""),
        ],
        "product_category_name string, product_category_name_english string",
    )

    resultado = silver.transformar_translation(df)

    assert set(resultado.columns) == {"product_category_name", "categoria_en"}
    linhas = {r["product_category_name"]: r["categoria_en"] for r in resultado.collect()}
    assert linhas == {"moveis": "furniture", "": None}


def test_products_tipa_e_renomeia(spark):
    df = spark.createDataFrame(
        [(" p1 ", " Toys ", "40", "100", "3", "500", "10", "5", "8")],
        (
            "product_id string, product_category_name string, product_name_lenght string, "
            "product_description_lenght string, product_photos_qty string, product_weight_g string, "
            "product_length_cm string, product_height_cm string, product_width_cm string"
        ),
    )

    resultado = silver.transformar_products(df)

    assert set(resultado.columns) == {
        "product_id",
        "product_category_name",
        "fotos_qty",
        "peso_g",
        "comprimento_cm",
        "altura_cm",
        "largura_cm",
    }
    linha = _unica_linha(resultado)
    assert linha["product_id"] == "p1"
    assert linha["product_category_name"] == "toys"
    assert linha["fotos_qty"] == 3
    assert linha["peso_g"] == 500
    tipos = dict(resultado.dtypes)
    assert tipos["fotos_qty"] == "int"
    assert tipos["peso_g"] == "int"


def test_customers_normaliza(spark):
    df = spark.createDataFrame(
        [(" c1 ", " u1 ", " 01001 ", " SAO PAULO ", " sp ")],
        (
            "customer_id string, customer_unique_id string, customer_zip_code_prefix string, "
            "customer_city string, customer_state string"
        ),
    )

    linha = _unica_linha(silver.transformar_customers(df))

    assert linha["customer_id"] == "c1"
    assert linha["customer_unique_id"] == "u1"
    assert linha["customer_zip_code_prefix"] == "01001"
    assert linha["customer_city"] == "sao paulo"
    assert linha["customer_state"] == "SP"


def test_sellers_normaliza(spark):
    df = spark.createDataFrame(
        [(" s1 ", " SAO PAULO ", " sp ", " 02002 ")],
        (
            "seller_id string, seller_city string, seller_state string, "
            "seller_zip_code_prefix string"
        ),
    )

    linha = _unica_linha(silver.transformar_sellers(df))

    assert linha["seller_id"] == "s1"
    assert linha["seller_city"] == "sao paulo"
    assert linha["seller_state"] == "SP"
    assert linha["seller_zip_code_prefix"] == "02002"


def test_orders_converte_timestamps_e_normaliza_status(spark):
    df = spark.createDataFrame(
        [
            (
                " o1 ",
                " c1 ",
                " DELIVERED ",
                "2017-01-01 10:00:00",
                "2017-01-01 11:00:00",
                "2017-01-02 10:00:00",
                "2017-01-03 10:00:00",
                "2017-01-05 10:00:00",
            )
        ],
        (
            "order_id string, customer_id string, order_status string, "
            "order_purchase_timestamp string, order_approved_at string, "
            "order_delivered_carrier_date string, order_delivered_customer_date string, "
            "order_estimated_delivery_date string"
        ),
    )

    resultado = silver.transformar_orders(df)

    linha = _unica_linha(resultado)
    assert linha["order_id"] == "o1"
    assert linha["order_status"] == "delivered"
    assert linha["order_purchase_timestamp"] == datetime(2017, 1, 1, 10, 0, 0)
    assert dict(resultado.dtypes)["order_purchase_timestamp"] == "timestamp"


def test_items_tipa_decimal_e_timestamp(spark):
    df = spark.createDataFrame(
        [(" o1 ", " 1 ", " p1 ", " s1 ", "2017-01-02 10:00:00", "10.50", "2.00")],
        (
            "order_id string, order_item_id string, product_id string, seller_id string, "
            "shipping_limit_date string, price string, freight_value string"
        ),
    )

    resultado = silver.transformar_items(df)

    linha = _unica_linha(resultado)
    assert linha["order_id"] == "o1"
    assert linha["order_item_id"] == "1"
    assert linha["price"] == Decimal("10.50")
    assert linha["freight_value"] == Decimal("2.00")
    tipos = dict(resultado.dtypes)
    assert tipos["price"] == "decimal(12,2)"
    assert tipos["freight_value"] == "decimal(12,2)"
    assert tipos["shipping_limit_date"] == "timestamp"


def test_payments_tipa(spark):
    df = spark.createDataFrame(
        [(" o1 ", "1", " CREDIT_CARD ", "2", "10.50")],
        (
            "order_id string, payment_sequential string, payment_type string, "
            "payment_installments string, payment_value string"
        ),
    )

    resultado = silver.transformar_payments(df)

    linha = _unica_linha(resultado)
    assert linha["order_id"] == "o1"
    assert linha["payment_sequential"] == 1
    assert linha["payment_type"] == "credit_card"
    assert linha["payment_installments"] == 2
    assert linha["payment_value"] == Decimal("10.50")
    tipos = dict(resultado.dtypes)
    assert tipos["payment_sequential"] == "int"
    assert tipos["payment_value"] == "decimal(12,2)"
