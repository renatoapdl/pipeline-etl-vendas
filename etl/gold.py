"""Camada Gold - modelo estrela para análises SQL.

Espelha a estrela definida em sql/07_esquema_estrela.sql:
2 dimensões (cliente, produto) + 1 fato (vendas).

A categoria fica dentro de dim_produto: é atributo do produto, não
dimensão à parte (dimensão separada seria snowflake).
"""
from __future__ import annotations

from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def _gerar_dimensoes(silver: DataFrame) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Gera dim_cliente, dim_produto e fato_vendas a partir do Silver."""
    w_cliente = Window.orderBy("id_cliente")
    dim_cliente = (
        silver.select("id_cliente")
        .distinct()
        .withColumn("cod_cliente", F.row_number().over(w_cliente))
    )

    w_produto = Window.orderBy("categoria", "produto")
    dim_produto = (
        silver.select("produto", "categoria")
        .distinct()
        .withColumn("cod_produto", F.row_number().over(w_produto))
    )

    # Left join: venda que achar dim acesa o codigo, venda sem match fica
    # com cod nulo (sinal de dado ruim) em vez de sumir do fato.
    fato_vendas = (
        silver.join(dim_cliente, "id_cliente", "left")
        .join(dim_produto, ["produto", "categoria"], "left")
        .select(
            "id_venda",
            "data_venda",
            "cod_cliente",
            "cod_produto",
            "canal",
            "quantidade",
            "valor_unitario",
            "valor_total",
        )
        .orderBy("id_venda")
    )

    return dim_cliente, dim_produto, fato_vendas


def gravar_gold(silver: DataFrame, saida_gold: Path) -> dict[str, Path]:
    """Cria e grava a camada Gold (dimensões + fato) em Parquet."""
    saida_gold.mkdir(parents=True, exist_ok=True)
    dim_cliente, dim_produto, fato = _gerar_dimensoes(silver)

    tabelas = {
        "dim_cliente": dim_cliente,
        "dim_produto": dim_produto,
        "fato_vendas": fato,
    }
    for nome, df in tabelas.items():
        (
            df.write.mode("overwrite")
            .format("parquet")
            .option("compression", "snappy")
            .save(str(saida_gold / nome))
        )

    return {nome: saida_gold / nome for nome in tabelas}
