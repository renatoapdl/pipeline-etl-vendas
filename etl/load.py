"""Grava o resultado em Parquet.

Por que Parquet e nao CSV: e coluna, comprimido e guarda o tipo da coluna. O CSV perde
tudo isso, e ainda quebra em valor que tem virgula (veja o valor "R$ 1.234,56" na entrada).

O modo overwrite torna a execucao idempotente: rodar duas vezes com o mesmo conteudo
produz o mesmo resultado, sem duplicar linha. Reprocessar e seguro.
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
