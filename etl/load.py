"""Grava o resultado em Parquet.

O modo overwrite torna a execucao idempotente.
"""
from pathlib import Path

from pyspark.sql import DataFrame


def gravar_parquet(df: DataFrame, destino: Path) -> Path:
    """Grava o DataFrame em Parquet e devolve o caminho final."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    (
        df.write.mode("overwrite")
        .format("parquet")
        .option("compression", "snappy")
        .save(str(destino))
    )
    return destino
