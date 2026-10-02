"""Testes das regras de limpeza.

Cada teste monta um DataFrame minimo com um tipo de sujeira e verifica que a regra
resolve. Roda em Spark local, entao precisa do Java instalado.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

pyspark = pytest.importorskip("pyspark", reason="pyspark nao instalado")

from pyspark.sql import SparkSession  # noqa: E402

from etl import transform  # noqa: E402

CABECALHO = (
    "id_venda string, id_cliente string, data_venda string, produto string, "
    "categoria string, quantidade string, valor_unitario string, canal string, situacao string"
)


@pytest.fixture(scope="session")
def spark():
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    sessao = (
        SparkSession.builder.master("local[1]")
        .appName("testes-etl-vendas")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )
    yield sessao
    sessao.stop()


def _linha(df, id_venda):
    return next(r for r in df.collect() if r["id_venda"] == id_venda)


def test_valor_com_moeda_e_virgula_vira_numero(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "2026-01-05", "mouse", "perifericos", "1", "R$ 1.234,56", "web", "aprovado")],
        CABECALHO,
    )
    assert _linha(transform.converter_valores(df), "V1")["valor_unitario"] == 1234.56


def test_data_em_dia_mes_ano_vira_date(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "17/02/2026", "mouse", "perifericos", "1", "10,00", "web", "aprovado")],
        CABECALHO,
    )
    linha = _linha(transform.padronizar_datas(df), "V1")
    assert linha["data_venda"].isoformat() == "2026-02-17"


def test_texto_com_espaco_e_caixa_alta_e_normalizado(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "2026-01-05", "  Notebook  ", "Periféricos", "1", "10,00", "  Web ", "aprovado")],
        CABECALHO,
    )
    linha = _linha(transform.normalizar_texto(df), "V1")
    assert linha["produto"] == "notebook"
    assert linha["canal"] == "web"
    assert linha["categoria"] == "periféricos"


def test_duplicada_mantem_a_data_mais_recente(spark):
    df = spark.createDataFrame(
        [
            ("V1", "C1", "2026-01-05", "mouse", "perifericos", "1", "10,00", "web", "aprovado"),
            ("V1", "C1", "2026-03-05", "mouse", "perifericos", "1", "20,00", "web", "aprovado"),
        ],
        CABECALHO,
    )
    resultado = transform.remover_duplicadas(
        transform.padronizar_datas(transform.converter_valores(df))
    )
    assert resultado.count() == 1
    linha = _linha(resultado, "V1")
    assert linha["data_venda"].isoformat() == "2026-03-05"
    assert linha["valor_unitario"] == 20.00


@pytest.mark.parametrize("situacao", [None, ""])
def test_nulos_recebem_valor_padrao(spark, situacao):
    df = spark.createDataFrame(
        [("V1", "C1", "2026-01-05", "mouse", "perifericos", "", "10,00", "web", situacao)],
        CABECALHO,
    )
    linha = _linha(transform.preencher_nulos(df), "V1")
    assert linha["quantidade"] == 1
    assert linha["situacao"] == "desconhecida"


def test_valor_sem_preco_permanece_nulo(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "2026-01-05", "mouse", "perifericos", "2", None, "web", "aprovado")],
        CABECALHO,
    )
    linha = _linha(transform.criar_valor_total(transform.converter_valores(df)), "V1")
    assert linha["valor_unitario"] is None
    assert linha["valor_total"] is None


def test_valor_total_derivado(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "2026-01-05", "mouse", "perifericos", "3", "10,50", "web", "aprovado")],
        CABECALHO,
    )
    convertido = transform.preencher_nulos(transform.converter_valores(df))
    assert _linha(transform.criar_valor_total(convertido), "V1")["valor_total"] == 31.50


def test_linha_sem_id_ou_sem_data_e_descartada(spark):
    df = spark.createDataFrame(
        [
            ("V1", "C1", "2026-01-05", "mouse", "perifericos", "1", "10,00", "web", "aprovado"),
            ("", "C2", "2026-01-05", "teclado", "perifericos", "1", "10,00", "web", "aprovado"),
            ("V3", "C3", "", "monitor", "informatica", "1", "10,00", "web", "aprovado"),
        ],
        CABECALHO,
    )
    assert transform.descartar_incompletos(df).count() == 1
