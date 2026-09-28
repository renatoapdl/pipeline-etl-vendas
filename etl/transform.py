"""Limpeza e transformacao das vendas.

  R1 descartar_incompletos  
  R2 padronizar_datas       
  R3 converter_valores      
  R4 normalizar_texto       
  R5 preencher_nulos       
  R6 remover_duplicadas    
  D1 criar_valor_total     
"""
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import (
    coalesce,
    col,
    lit,
    lower,
    regexp_replace,
    round as arredondar,
    row_number,
    to_date,
    trim,
    when,
)

FORMATOS_DATA = {"iso": "yyyy-MM-dd", "brasileiro": "dd/MM/yyyy"}


def descartar_incompletos(df: DataFrame) -> DataFrame:   
    return df.filter(trim(col("id_venda")) != "").filter(trim(col("data_venda")) != "")


def padronizar_datas(df: DataFrame) -> DataFrame:
    texto = trim(col("data_venda"))
    return df.withColumn(
        "data_venda",
        when(texto.rlike(r"^\d{2}/\d{2}/\d{4}$"), to_date(texto, "dd/MM/yyyy")).otherwise(
            to_date(texto, "yyyy-MM-dd")
        ),
    )


def converter_valores(df: DataFrame) -> DataFrame:
    limpo = regexp_replace(trim(col("valor_unitario")), r"[^0-9,]", "")
    com_ponto = regexp_replace(limpo, r"\.", "")
    return df.withColumn("valor_unitario", regexp_replace(com_ponto, ",", ".").cast("double"))


def normalizar_texto(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("produto", lower(trim(col("produto"))))
        .withColumn("categoria", lower(trim(col("categoria"))))
        .withColumn("canal", lower(trim(col("canal"))))
        .withColumn("situacao", lower(trim(col("situacao"))))
    )


def preencher_nulos(df: DataFrame) -> DataFrame:
    situacao_vazia = col("situacao").isNull() | (trim(col("situacao")) == "")
    return (
        df.withColumn("quantidade", coalesce(col("quantidade").cast("int"), lit(1)))
        .withColumn(
            "situacao", when(situacao_vazia, "desconhecida").otherwise(trim(col("situacao")))
        )
    )


def remover_duplicadas(df: DataFrame) -> DataFrame:
    janela = Window.partitionBy("id_venda").orderBy(col("data_venda").desc())
    return (
        df.withColumn("_rank", row_number().over(janela))
        .filter(col("_rank") == 1)
        .drop("_rank")
    )


def criar_valor_total(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "valor_total", arredondar(col("quantidade") * col("valor_unitario"), 2)
    )


def tratar(df: DataFrame) -> DataFrame:
    df = descartar_incompletos(df)
    df = padronizar_datas(df)
    df = converter_valores(df)
    df = normalizar_texto(df)
    df = preencher_nulos(df)
    df = remover_duplicadas(df)
    return criar_valor_total(df)
