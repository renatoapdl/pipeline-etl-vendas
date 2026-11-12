import os
import sys

import pytest
from pyspark.sql import SparkSession

# No Windows, o Spark chamaria o "python" do PATH (alias da Microsoft Store).
# Força os workers a usarem o mesmo interpretador do pytest (o do venv).
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.appName("pytest-etl-olist")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()
