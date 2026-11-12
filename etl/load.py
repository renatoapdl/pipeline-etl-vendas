"""Grava o resultado em Parquet.

O modo overwrite torna a execucao idempotente.
"""
import shutil
import tempfile
import time
from pathlib import Path

from pyspark.sql import DataFrame


def _remover_se_existe(caminho: Path) -> None:
    """Remove diretório no Windows com retry (lock do Spark/JVM)."""
    if not caminho.exists():
        return
    for _ in range(5):
        try:
            shutil.rmtree(caminho)
            return
        except PermissionError:
            time.sleep(0.5)
    shutil.rmtree(caminho, ignore_errors=True)


def gravar_parquet(df: DataFrame, destino: Path) -> Path:
    """Grava o DataFrame em Parquet e devolve o caminho final.
    
    No Windows, grava em temp e move para evitar lock do Spark/JVM.
    """
    _remover_se_existe(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    
    # Grava em diretório temporário e move (evita lock do overwrite no Windows)
    with tempfile.TemporaryDirectory(prefix="spark_write_", dir=destino.parent) as tmp:
        tmp_path = Path(tmp) / destino.name
        (
            df.write.mode("overwrite")
            .format("parquet")
            .option("compression", "snappy")
            .save(str(tmp_path))
        )
        _remover_se_existe(destino)
        if destino.exists():
            raise RuntimeError(
                f"Não foi possível remover o destino (possível lock do Windows): {destino}"
            )
        shutil.move(str(tmp_path), str(destino))
    
    return destino
