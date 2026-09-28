"""Le o CSV de vendas exatamente como ele chegou, sem corrigir nada.

Regra da camada: quem extrai nao arruma dado. A correcao acontece na transformacao, e
assim da para conferir o que foi limpo comparando os dois Parquet.

O schema é declarado com todas as colunas como texto de proposito. Se eu deixasse o Spark
inferir o tipo, a coluna valor_unitario viraria string numa linha e double na outra, porque
o arquivo mistura 3500.00, "R$ 1.234,56" e "89,90". Lendo tudo como texto, eu escolho
explicitamente onde cada coluna vira numero.
"""
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType, StructField, StructType

SCHEMA = StructType(
    [
        StructField("id_venda", StringType(), True),
        StructField("id_cliente", StringType(), True),
        StructField("data_venda", StringType(), True),
        StructField("produto", StringType(), True),
        StructField("categoria", StringType(), True),
        StructField("quantidade", StringType(), True),
        StructField("valor_unitario", StringType(), True),
        StructField("canal", StringType(), True),
        StructField("situacao", StringType(), True),
    ]
)


def ler_vendas(spark: SparkSession, caminho: Path) -> DataFrame:
    """Le o CSV com o cabecalho da primeira linha e o schema declarado acima."""
    if not caminho.exists():
        raise SystemExit(f"CSV nao encontrado: {caminho}")

    return (
        spark.read.option("header", True)
        .option("encoding", "UTF-8")
        .option("delimiter", ",")
        .schema(SCHEMA)
        .csv(str(caminho))
    )
