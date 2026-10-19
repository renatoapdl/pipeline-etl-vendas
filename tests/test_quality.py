"""Testes do quality gate."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

pyspark = pytest.importorskip("pyspark", reason="pyspark nao instalado")

from pyspark.sql import SparkSession  # noqa: E402

from etl import quality, transform  # noqa: E402

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
        .appName("testes-quality")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )
    yield sessao
    sessao.stop()


def _silver(df):
    return transform.criar_valor_total(
        transform.preencher_nulos(
            transform.normalizar_texto(
                transform.converter_valores(transform.padronizar_datas(df))
            )
        )
    )


def test_quality_aprova_base_valida(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "2026-01-05", "mouse", "perifericos", "2", "10,00", "web", "aprovado")],
        CABECALHO,
    )
    relatorio = quality.verificar_silver(_silver(df))
    assert relatorio.tem_erros is False
    quality.garantir(relatorio)


def test_quality_reprova_data_invalida(spark):
    df = spark.createDataFrame(
        [("V1", "C1", "31/31/2026", "mouse", "perifericos", "1", "10,00", "web", "aprovado")],
        CABECALHO,
    )
    relatorio = quality.verificar_silver(_silver(df))
    assert relatorio.tem_erros is True
    assert any("data_venda" in erro for erro in relatorio.erros)
    with pytest.raises(quality.QualityError):
        quality.garantir(relatorio)
