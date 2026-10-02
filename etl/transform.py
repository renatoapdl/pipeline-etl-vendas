from pyspark.sql import DataFrame 
from pyspark.sql.functions import (
    col,
    when,
    to_date,
    trim,
    regexp_replace,
    replace,
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
    return df.withColumn("valor_unitario", replace(limpo, ",", ".").cast("double"))
