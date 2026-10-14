from pyspark.sql import DataFrame, Window 
from pyspark.sql.functions import (
    col,
    when,
    to_date,
    trim,
    regexp_replace,
    lower,
    lit,
    row_number,
    round as arredondar,
)


def descartar_incompletos(df: DataFrame) -> DataFrame:
    return df.filter(trim(col("id_venda")) !="").filter(trim(col("data_venda")) !="")


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
    return df.withColumn("valor_unitario", regexp_replace(limpo, ",", ".").cast("double"))


def normalizar_texto(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("produto", lower(trim(col("produto"))))
        .withColumn("categoria", lower(trim(col("categoria"))))
        .withColumn("canal", lower(trim(col("canal"))))
        .withColumn("situacao", lower(trim(col("situacao"))))
    )


def preencher_nulos(df: DataFrame) -> DataFrame:
    qtd_vazia = col("quantidade").isNull() | (trim(col("quantidade")) == "")
    sit_vazia = col("situacao").isNull() | (trim(col("situacao")) == "")
    return (
        df.withColumn("quantidade", when(qtd_vazia, lit(1)).otherwise(col("quantidade").cast("int")))
        .withColumn("situacao", when(sit_vazia, lit("desconhecida")).otherwise(lower(trim(col("situacao")))))
    )



def remover_duplicadas(df: DataFrame) -> DataFrame:
    janela = Window.partitionBy("id_venda").orderBy(col("data_venda").desc())
    df_com_numero = df.withColumn("rn", row_number().over(janela))
    return df_com_numero.filter(col("rn") == 1).drop("rn")



def criar_valor_total(df: DataFrame) -> DataFrame:
    return df.withColumn("valor_total", arredondar(col("quantidade") * col("valor_unitario"), 2))