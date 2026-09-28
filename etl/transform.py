"""Limpeza e transformacao das vendas. Uma regra por funcao, na ordem em que rodam.

As regras sao as que o CSV de entrada exige. Nada aqui e generico "por precaucao": cada
funcao existe porque existe uma linha suja no arquivo de entrada.

  R1 descartar_incompletos  sem id_venda ou sem data_venda: nao da para corrigir, va fora
  R2 padronizar_datas       2026-01-05 e 17/02/2026 viram o mesmo tipo (date)
  R3 converter_valores      "R$ 1.234,56" vira 1234.56
  R4 normalizar_texto       "  Notebook  " e "CABO USB" viram "notebook" e "cabo usb"
  R5 preencher_nulos       quantidade vazia vira 1, situacao vazia vira "desconhecida"
  R6 remover_duplicadas    a mesma venda chega duas vezes: fica a mais recente
  D1 criar_valor_total     campo derivado: quantidade * valor_unitario
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
    """R1: sem id_venda ou sem data_venda a linha nao presta e e removida.

    O filtro roda sobre o texto, antes de converter data. Depois de converter, data
    invalida viraria nulo e a linha passaria despercebida.
    """
    return df.filter(trim(col("id_venda")) != "").filter(trim(col("data_venda")) != "")


def padronizar_datas(df: DataFrame) -> DataFrame:
    """R2: as duas datas do arquivo viram uma coluna do tipo date.

    O PySpark aceita um formato so por chamada, entao o `when` escolhe o formato antes de
    converter. Se a data nao estiver em nenhum dos dois, vira nulo e o run.py avisa.
    """
    texto = trim(col("data_venda"))
    return df.withColumn(
        "data_venda",
        when(texto.rlike(r"^\d{2}/\d{2}/\d{4}$"), to_date(texto, "dd/MM/yyyy")).otherwise(
            to_date(texto, "yyyy-MM-dd")
        ),
    )


def converter_valores(df: DataFrame) -> DataFrame:
    """R3: tira o prefixo de moeda e troca o separador de milhar.

    O arquivo de origem e brasileiro, entao o formato e sempre "1.234,56": ponto e
    milhar, virgula e decimal. "R$ 1.234,56" vira 1234.56 em tres passos: remove o "R$",
    remove o ponto de milhar e troca a virgula decimal por ponto.

    Por que o CSV esta todo nesse formato, e nao misturado: na primeira versao eu deixei
    parte dos valores como 189.90 e o resultado saiu 18990.0, porque o ponto de quem le
    o CSV como milhar e o ponto de quem le como decimal se confundem. A saida correta
    para um arquivo brasileiro depende do sistema de origem, e adivinhar um numero e
    pior do que exigir um formato unico.
    """
    limpo = regexp_replace(trim(col("valor_unitario")), r"[^0-9,]", "")
    com_ponto = regexp_replace(limpo, r"\.", "")
    return df.withColumn("valor_unitario", regexp_replace(com_ponto, ",", ".").cast("double"))


def normalizar_texto(df: DataFrame) -> DataFrame:
    """R4: espaco nas pontas e caixa alta quebram agrupamento por produto e por canal."""
    return (
        df.withColumn("produto", lower(trim(col("produto"))))
        .withColumn("categoria", lower(trim(col("categoria"))))
        .withColumn("canal", lower(trim(col("canal"))))
        .withColumn("situacao", lower(trim(col("situacao"))))
    )


def preencher_nulos(df: DataFrame) -> DataFrame:
    """R5: valor padrao explicito para campo vazio, coerente com o significado da coluna.

    quantidade vazia assume 1 (uma venda sem quantidade e uma venda de uma unidade) e
    situacao vazia vira "desconhecida", que e um rotulo honesto e continua filtravel.

    Dois detalhes que custaram uma execucao para achar: o CSV traz campo vazio como NULO,
    e nao como texto vazio, entao a regra precisa checar os dois (null e ""). A primeira
    versao so checava "" e o teste passava, porque o teste montava o DataFrame com texto
    vazio; o dado real deixava situacao nula. E "desconhecida" precisa ser rotulo de
    verdade, senao o filtro por situacao volta a nao pegar essa linha.
    """
    situacao_vazia = col("situacao").isNull() | (trim(col("situacao")) == "")
    return (
        df.withColumn("quantidade", coalesce(col("quantidade").cast("int"), lit(1)))
        .withColumn(
            "situacao", when(situacao_vazia, "desconhecida").otherwise(trim(col("situacao")))
        )
    )


def remover_duplicadas(df: DataFrame) -> DataFrame:
    """R6: uma linha por id_venda, mantendo a de data mais recente.

    dropDuplicates sozinho guardaria qualquer uma das duas, na ordem em que o Spark
    ler. Com Window + row_number a escolha e explicita e deterministica.
    """
    janela = Window.partitionBy("id_venda").orderBy(col("data_venda").desc())
    return (
        df.withColumn("_rank", row_number().over(janela))
        .filter(col("_rank") == 1)
        .drop("_rank")
    )


def criar_valor_total(df: DataFrame) -> DataFrame:
    """D1: campo derivado a partir de dois campos de origem."""
    return df.withColumn(
        "valor_total", arredondar(col("quantidade") * col("valor_unitario"), 2)
    )


def tratar(df: DataFrame) -> DataFrame:
    """Executa as regras na ordem. Chamar em partes, para mostrar o efeito de cada uma."""
    df = descartar_incompletos(df)
    df = padronizar_datas(df)
    df = converter_valores(df)
    df = normalizar_texto(df)
    df = preencher_nulos(df)
    df = remover_duplicadas(df)
    return criar_valor_total(df)
