"""Camada Gold - modelo estrela para análises SQL.
"""
from __future__ import annotations

from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def _gerar_dimensoes(silver: DataFrame) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Gera dimensões categoria/canal e fato vendas (star schema)."""
    w_cat = Window.orderBy("nome_categoria")
    dim_categoria = (
        silver.select(F.col("categoria").alias("nome_categoria"))
        .distinct()
        .withColumn("cod_categoria", F.row_number().over(w_cat))
    )

    w_canal = Window.orderBy("nome_canal")
    dim_canal = (
        silver.select(F.col("canal").alias("nome_canal"))
        .distinct()
        .withColumn("cod_canal", F.row_number().over(w_canal))
    )

    fato_vendas = (
        silver.join(dim_categoria, silver.categoria == dim_categoria.nome_categoria, "left")
        .join(dim_canal, silver.canal == dim_canal.nome_canal, "left")
        .select(
            "id_venda",
            "data_venda",
            "cod_categoria",
            "cod_canal",
            "quantidade",
            "valor_unitario",
            "valor_total",
        )
        .orderBy("id_venda")
    )

    return dim_categoria, dim_canal, fato_vendas


def gravar_gold(silver: DataFrame, saida_gold: Path) -> dict[str, Path]:
    """Cria e grava camadas Gold (dimensões + fato)."""
    saida_gold.mkdir(parents=True, exist_ok=True)
    dim_cat, dim_canal, fato = _gerar_dimensoes(silver)

    (
        dim_cat.write.mode("overwrite")
        .format("parquet")
        .option("compression", "snappy")
        .save(str(saida_gold / "dim_categoria"))
    )
    (
        dim_canal.write.mode("overwrite")
        .format("parquet")
        .option("compression", "snappy")
        .save(str(saida_gold / "dim_canal"))
    )
    (
        fato.write.mode("overwrite")
        .format("parquet")
        .option("compression", "snappy")
        .save(str(saida_gold / "fato_vendas"))
    )

    return {
        "dim_categoria": saida_gold / "dim_categoria",
        "dim_canal": saida_gold / "dim_canal",
        "fato_vendas": saida_gold / "fato_vendas",
    }
