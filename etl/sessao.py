"""Sessão Spark compartilhada pelos módulos do Olist."""

import os

from pyspark.sql import SparkSession


def get_spark(app_name: str = "etl-olist"):
    """Sessão Spark local."""

    builder = SparkSession.builder.appName(app_name).config(
        "spark.sql.session.timeZone", "America/Fortaleza"
    )
    if "PYSPARK_GATEWAY_PORT" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()

