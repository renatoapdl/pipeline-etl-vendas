"""Quality gate do pipeline Olist — valida Silver e Gold antes de publicar.

As funções recebem DataFrames já em memória (sem ler do disco), para poderem
ser testadas no CI, onde os Parquets e os CSVs reais não existem.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

TABELAS_SILVER = [
    "translation",
    "products",
    "customers",
    "sellers",
    "orders",
    "items",
    "payments",
]


# Relatório simples: acumula linhas OK/AVISO/ERRO e sinaliza se houve erro
class Relatorio:
    def __init__(self) -> None:
        self._linhas: list[str] = []
        self.tem_erros = False

    def ok(self, mensagem: str) -> None:
        self._linhas.append(f"OK    {mensagem}")

    def erro(self, mensagem: str) -> None:
        self._linhas.append(f"ERRO  {mensagem}")
        self.tem_erros = True

    def aviso(self, mensagem: str) -> None:
        self._linhas.append(f"AVISO {mensagem}")

    def linhas(self) -> list[str]:
        return self._linhas


# Verificações genéricas
def _verificar_nao_vazio(rel: Relatorio, nome: str, total: int) -> None:
    if total == 0:
        rel.erro(f"{nome}: tabela vazia")
    else:
        rel.ok(f"{nome}: {total} linhas")


def _verificar_sem_duplicata(
    rel: Relatorio, nome: str, df: DataFrame, chaves: list[str]
) -> None:
    duplicadas = df.groupBy(*chaves).count().where(F.col("count") > 1).count()
    if duplicadas:
        rel.erro(f"{nome}: {duplicadas} chaves duplicadas em {chaves}")
    else:
        rel.ok(f"{nome}: grão {chaves} sem duplicatas")


def _verificar_sem_nulo(
    rel: Relatorio, nome: str, df: DataFrame, colunas: list[str]
) -> None:
    for coluna in colunas:
        nulos = df.where(F.col(coluna).isNull()).count()
        if nulos:
            rel.erro(f"{nome}: {nulos} nulos em {coluna}")
        else:
            rel.ok(f"{nome}: {coluna} sem nulos")


def _verificar_soma(rel: Relatorio, nome: str, valor_gold, valor_silver) -> None:
    if valor_gold != valor_silver:
        rel.erro(f"{nome}: Gold={valor_gold} != Silver={valor_silver}")
    else:
        rel.ok(f"{nome}: {valor_gold} (== Silver)")


# Validação da camada Silver
def verificar_silver(tabelas: dict[str, DataFrame]) -> Relatorio:
    rel = Relatorio()

    for nome in TABELAS_SILVER:
        _verificar_nao_vazio(rel, nome, tabelas[nome].count())

    _verificar_sem_duplicata(rel, "customers", tabelas["customers"], ["customer_id"])
    _verificar_sem_duplicata(rel, "sellers", tabelas["sellers"], ["seller_id"])
    _verificar_sem_duplicata(rel, "orders", tabelas["orders"], ["order_id"])
    _verificar_sem_duplicata(
        rel, "items", tabelas["items"], ["order_id", "order_item_id"]
    )
    _verificar_sem_duplicata(
        rel, "payments", tabelas["payments"], ["order_id", "payment_sequential"]
    )

    _verificar_sem_nulo(
        rel, "customers", tabelas["customers"], ["customer_id", "customer_unique_id"]
    )
    _verificar_sem_nulo(rel, "sellers", tabelas["sellers"], ["seller_id"])
    _verificar_sem_nulo(
        rel,
        "orders",
        tabelas["orders"],
        ["order_id", "customer_id", "order_purchase_timestamp"],
    )
    _verificar_sem_nulo(
        rel,
        "items",
        tabelas["items"],
        ["order_id", "order_item_id", "product_id", "seller_id"],
    )
    _verificar_sem_nulo(
        rel, "payments", tabelas["payments"], ["order_id", "payment_sequential"]
    )
    _verificar_sem_nulo(rel, "products", tabelas["products"], ["product_id"])

    return rel


# Validação da camada Gold (tabelas em memória, antes de publicar)
def verificar_gold(
    tabelas_gold: dict[str, DataFrame], tabelas_silver: dict[str, DataFrame]
) -> Relatorio:
    rel = Relatorio()
    itens = tabelas_gold["fato_itens"]
    pagamentos = tabelas_gold["fato_pagamentos"]
    silver_items = tabelas_silver["items"]
    silver_payments = tabelas_silver["payments"]

    _verificar_sem_duplicata(rel, "fato_itens", itens, ["order_id", "order_item_id"])
    _verificar_sem_duplicata(
        rel, "fato_pagamentos", pagamentos, ["order_id", "payment_sequential"]
    )

    _verificar_sem_nulo(
        rel, "fato_itens", itens, ["cod_cliente", "cod_produto", "cod_vendedor", "cod_data"]
    )
    _verificar_sem_nulo(rel, "fato_pagamentos", pagamentos, ["cod_cliente", "cod_data"])

    # Contagem: os fatos não podem perder linhas em relação ao Silver
    total_itens = itens.count()
    total_silver_items = silver_items.count()
    if total_itens != total_silver_items:
        rel.erro(f"fato_itens: {total_itens} linhas != {total_silver_items} no Silver items")
    else:
        rel.ok(f"fato_itens: {total_itens} linhas (== Silver items)")

    total_pagamentos = pagamentos.count()
    total_silver_payments = silver_payments.count()
    if total_pagamentos != total_silver_payments:
        rel.erro(
            f"fato_pagamentos: {total_pagamentos} linhas != "
            f"{total_silver_payments} no Silver payments"
        )
    else:
        rel.ok(f"fato_pagamentos: {total_pagamentos} linhas (== Silver payments)")

    # Preservação de valores: o Gold não pode alterar somas do Silver
    _verificar_soma(
        rel,
        "fato_itens price",
        itens.agg(F.sum("price")).first()[0],
        silver_items.agg(F.sum("price")).first()[0],
    )
    _verificar_soma(
        rel,
        "fato_itens freight_value",
        itens.agg(F.sum("freight_value")).first()[0],
        silver_items.agg(F.sum("freight_value")).first()[0],
    )
    _verificar_soma(
        rel,
        "fato_pagamentos payment_value",
        pagamentos.agg(F.sum("payment_value")).first()[0],
        silver_payments.agg(F.sum("payment_value")).first()[0],
    )

    # Reconciliação por pedido (insight da base Olist, não bloqueia)
    itens_por_pedido = itens.groupBy("order_id").agg(
        F.sum(F.col("price") + F.col("freight_value")).alias("valor_itens")
    )
    pagamentos_por_pedido = pagamentos.groupBy("order_id").agg(
        F.sum("payment_value").alias("valor_pagamentos")
    )
    divergencias = (
        itens_por_pedido.join(pagamentos_por_pedido, "order_id", "inner")
        .withColumn("dif", F.col("valor_itens") - F.col("valor_pagamentos"))
        .where(F.abs("dif") > F.lit(0.01))
    )
    divergentes = divergencias.count()
    if divergentes:
        soma_abs = divergencias.agg(F.sum(F.abs("dif"))).first()[0]
        rel.aviso(
            f"reconciliação: {divergentes} pedidos com price+frete != payment_value "
            f"(diferença da base Olist, soma abs {soma_abs})"
        )
    else:
        rel.ok("reconciliação: price+frete == payment_value por pedido (com item)")

    return rel
