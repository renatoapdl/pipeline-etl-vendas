"""Quality gate das camadas Silver e Gold.

Checagens de severidade ERROR bloqueiam a publicacao do Gold; as de
severidade WARN apenas aparecem no relatorio.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


@dataclass
class Relatorio:
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    @property
    def tem_erros(self) -> bool:
        return bool(self.erros)

    def linhas(self) -> list[str]:
        linhas = [f"ERRO: {erro}" for erro in self.erros]
        linhas += [f"AVISO: {aviso}" for aviso in self.avisos]
        return linhas or ["nenhum problema encontrado"]


class QualityError(RuntimeError):
    def __init__(self, relatorio: Relatorio):
        self.relatorio = relatorio
        super().__init__("quality gate bloqueou a publicacao")


def _faltando(df: DataFrame, coluna: str) -> int:
    valor = F.col(coluna)
    return df.filter(valor.isNull() | (F.trim(valor) == "")).count()


def _erro_se(relatorio: Relatorio, quantidade: int, mensagem: str) -> None:
    if quantidade:
        relatorio.erros.append(f"{quantidade} {mensagem}")


def _aviso_se(relatorio: Relatorio, quantidade: int, mensagem: str) -> None:
    if quantidade:
        relatorio.avisos.append(f"{quantidade} {mensagem}")


def verificar_silver(df: DataFrame) -> Relatorio:
    relatorio = Relatorio()

    _erro_se(relatorio, _faltando(df, "id_venda"), "linha(s) sem id_venda")
    duplicadas = df.groupBy("id_venda").count().filter(F.col("count") > 1).count()
    _erro_se(relatorio, duplicadas, "id_venda duplicado(s)")
    _erro_se(
        relatorio,
        df.filter(F.col("data_venda").isNull()).count(),
        "linha(s) com data_venda nula ou invalida",
    )
    _erro_se(relatorio, _faltando(df, "id_cliente"), "linha(s) sem id_cliente")
    _erro_se(relatorio, _faltando(df, "produto"), "linha(s) sem produto")
    _erro_se(relatorio, _faltando(df, "categoria"), "linha(s) sem categoria")
    _erro_se(
        relatorio,
        df.filter(F.col("quantidade").isNull() | (F.col("quantidade") <= 0)).count(),
        "linha(s) com quantidade nula ou menor/igual a zero",
    )
    _erro_se(
        relatorio,
        df.filter(F.col("valor_unitario") < 0).count(),
        "linha(s) com valor_unitario negativo",
    )

    _aviso_se(
        relatorio,
        df.filter(F.col("valor_unitario").isNull()).count(),
        "linha(s) sem valor_unitario (valor_total fica nulo)",
    )
    _aviso_se(relatorio, _faltando(df, "canal"), "linha(s) sem canal")
    _aviso_se(
        relatorio,
        df.filter(F.col("situacao") == "desconhecida").count(),
        "linha(s) com situacao desconhecida",
    )
    _aviso_se(
        relatorio,
        df.filter(F.col("situacao").isin("cancelado", "pendente")).count(),
        "venda(s) cancelada(s) ou pendente(s)",
    )

    return relatorio


def verificar_gold(tabelas: dict[str, DataFrame], silver: DataFrame) -> Relatorio:
    relatorio = Relatorio()

    fato = tabelas["fato_vendas"]
    _erro_se(
        relatorio,
        abs(fato.count() - silver.count()),
        "linha(s) de diferenca entre Silver e fato_vendas",
    )
    _erro_se(
        relatorio,
        fato.filter(F.col("cod_cliente").isNull()).count(),
        "linha(s) do fato sem cod_cliente",
    )
    _erro_se(
        relatorio,
        fato.filter(F.col("cod_produto").isNull()).count(),
        "linha(s) do fato sem cod_produto",
    )

    dim_cliente = tabelas["dim_cliente"]
    dim_produto = tabelas["dim_produto"]
    _erro_se(
        relatorio,
        dim_cliente.count() - dim_cliente.select("cod_cliente").distinct().count(),
        "cod_cliente duplicado em dim_cliente",
    )
    _erro_se(
        relatorio,
        dim_produto.count() - dim_produto.select("cod_produto").distinct().count(),
        "cod_produto duplicado em dim_produto",
    )

    return relatorio


def garantir(relatorio: Relatorio) -> None:
    if relatorio.tem_erros:
        raise QualityError(relatorio)
