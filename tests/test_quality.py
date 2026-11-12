from datetime import datetime
from decimal import Decimal

from etl import quality


def _silver_completo(spark):
    return {
        "translation": spark.createDataFrame(
            [("moveis", "furniture")],
            "product_category_name string, categoria_en string",
        ),
        "products": spark.createDataFrame([("p1",)], "product_id string"),
        "customers": spark.createDataFrame(
            [("c1", "u1")], "customer_id string, customer_unique_id string"
        ),
        "sellers": spark.createDataFrame([("s1",)], "seller_id string"),
        "orders": spark.createDataFrame(
            [("o1", "c1", datetime(2017, 1, 5))],
            "order_id string, customer_id string, order_purchase_timestamp timestamp",
        ),
        "items": spark.createDataFrame(
            [("o1", "1", "p1", "s1", Decimal("10.00"), Decimal("2.00"))],
            (
                "order_id string, order_item_id string, product_id string, seller_id string, "
                "price decimal(12,2), freight_value decimal(12,2)"
            ),
        ),
        "payments": spark.createDataFrame(
            [("o1", 1, "credit_card", 2, Decimal("12.00"))],
            (
                "order_id string, payment_sequential int, payment_type string, "
                "payment_installments int, payment_value decimal(12,2)"
            ),
        ),
    }


def _gold_completo(spark):
    itens = spark.createDataFrame(
        [("o1", "1", 1, 10, 100, 20170105, Decimal("10.00"), Decimal("2.00"))],
        (
            "order_id string, order_item_id string, cod_cliente int, cod_produto int, "
            "cod_vendedor int, cod_data int, price decimal(12,2), freight_value decimal(12,2)"
        ),
    )
    pagamentos = spark.createDataFrame(
        [("o1", 1, 1, 20170105, "credit_card", 2, Decimal("12.00"))],
        (
            "order_id string, payment_sequential int, cod_cliente int, cod_data int, "
            "payment_type string, payment_installments int, payment_value decimal(12,2)"
        ),
    )
    return {"fato_itens": itens, "fato_pagamentos": pagamentos}


def test_relatorio_acumula_e_sinaliza_erro():
    rel = quality.Relatorio()
    rel.ok("tudo certo")
    rel.aviso("atencao")
    assert rel.tem_erros is False

    rel.erro("falhou")
    assert rel.tem_erros is True
    assert rel.linhas() == ["OK    tudo certo", "AVISO atencao", "ERRO  falhou"]


def test_verificar_silver_reprova_duplicata(spark):
    tabelas = _silver_completo(spark)
    tabelas["customers"] = spark.createDataFrame(
        [("c1", "u1"), ("c1", "u2")],
        "customer_id string, customer_unique_id string",
    )
    rel = quality.verificar_silver(tabelas)
    assert rel.tem_erros is True
    assert any("duplicadas" in linha for linha in rel.linhas())


def test_verificar_gold_reprova_contagem(spark):
    silver = _silver_completo(spark)
    silver["items"] = spark.createDataFrame(
        [
            ("o1", "1", "p1", "s1", Decimal("10.00"), Decimal("2.00")),
            ("o2", "1", "p1", "s1", Decimal("0.00"), Decimal("0.00")),
        ],
        (
            "order_id string, order_item_id string, product_id string, seller_id string, "
            "price decimal(12,2), freight_value decimal(12,2)"
        ),
    )
    rel = quality.verificar_gold(_gold_completo(spark), silver)
    assert rel.tem_erros is True
    assert any("fato_itens" in linha and "!=" in linha for linha in rel.linhas())


def test_verificar_silver_aprovado(spark):
    rel = quality.verificar_silver(_silver_completo(spark))
    assert rel.tem_erros is False


def test_verificar_silver_reprova_tabela_vazia(spark):
    tabelas = _silver_completo(spark)
    tabelas["items"] = spark.createDataFrame(
        [], "order_id string, order_item_id string, product_id string, seller_id string"
    )
    rel = quality.verificar_silver(tabelas)
    assert rel.tem_erros is True


def test_verificar_silver_reprova_nulo(spark):
    tabelas = _silver_completo(spark)
    tabelas["orders"] = spark.createDataFrame(
        [("o1", None, datetime(2017, 1, 5))],
        "order_id string, customer_id string, order_purchase_timestamp timestamp",
    )
    rel = quality.verificar_silver(tabelas)
    assert rel.tem_erros is True


def test_verificar_gold_aprovado(spark):
    rel = quality.verificar_gold(_gold_completo(spark), _silver_completo(spark))
    assert rel.tem_erros is False
    assert any(linha.startswith("OK    reconciliação") for linha in rel.linhas())


def test_verificar_gold_reprova_duplicata(spark):
    gold_tabelas = _gold_completo(spark)
    gold_tabelas["fato_itens"] = spark.createDataFrame(
        [
            ("o1", "1", 1, 10, 100, 20170105, Decimal("10.00"), Decimal("2.00")),
            ("o1", "1", 1, 10, 100, 20170105, Decimal("10.00"), Decimal("2.00")),
        ],
        (
            "order_id string, order_item_id string, cod_cliente int, cod_produto int, "
            "cod_vendedor int, cod_data int, price decimal(12,2), freight_value decimal(12,2)"
        ),
    )
    rel = quality.verificar_gold(gold_tabelas, _silver_completo(spark))
    assert rel.tem_erros is True
    assert any("duplicadas" in linha for linha in rel.linhas())


def test_verificar_gold_avisa_reconciliacao(spark):
    silver = _silver_completo(spark)
    silver["payments"] = spark.createDataFrame(
        [("o1", 1, "credit_card", 2, Decimal("99.00"))],
        (
            "order_id string, payment_sequential int, payment_type string, "
            "payment_installments int, payment_value decimal(12,2)"
        ),
    )
    gold_tabelas = _gold_completo(spark)
    gold_tabelas["fato_pagamentos"] = spark.createDataFrame(
        [("o1", 1, 1, 20170105, "credit_card", 2, Decimal("99.00"))],
        (
            "order_id string, payment_sequential int, cod_cliente int, cod_data int, "
            "payment_type string, payment_installments int, payment_value decimal(12,2)"
        ),
    )

    rel = quality.verificar_gold(gold_tabelas, silver)

    assert rel.tem_erros is False
    assert any(linha.startswith("AVISO reconciliação") for linha in rel.linhas())
