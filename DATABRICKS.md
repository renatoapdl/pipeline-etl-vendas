# Databricks CE: carregar o resultado do ETL

As queries em `sql/` não leem mais um CSV. Elas leem as tabelas criadas a partir do Parquet que o próprio ETL gera. Este arquivo é o passo a passo dessa carga.

## Por que mudou

Antes, a base do Databricks era o `dados/vendas_bruto_tratado_for_databricks.csv`: o CSV bruto com só a vírgula decimal trocada por ponto. Ou seja, as queries rodavam sobre dados sujos:

- `VEN-0004` e `VEN-0011` apareciam duas vezes, e as agregações contavam a duplicata;
- a linha sem `id_venda` e a sem `data_venda` ainda estavam lá;
- `  Notebook  ` e `CABO USB` sem normalizar quebravam o agrupamento.

Agora a fonte é a saída do pipeline: `silver.vendas` (limpa e tipada) e o modelo estrela em `gold.*`. O número do resultado muda para melhor, e passa a bater com o que o README descreve (27 → 23).

## O que subir

Depois de rodar `python etl/run.py`, cada tabela é uma pasta em `data/` com um `part-00000-*.parquet` (mais um `_SUCCESS` e arquivos `.crc`). Suba **só o `.parquet`**.

| Tabela no Databricks | Arquivo local |
|---|---|
| `silver.vendas` | `data/silver/vendas/part-00000-*.parquet` |
| `gold.dim_cliente` | `data/gold/dim_cliente/part-00000-*.parquet` |
| `gold.dim_produto` | `data/gold/dim_produto/part-00000-*.parquet` |
| `gold.fato_vendas` | `data/gold/fato_vendas/part-00000-*.parquet` |

## Passo a passo

### 1. Criar onde guardar os arquivos

No Databricks, num notebook ou no SQL Editor, crie os schemas e um volume para receber os Parquets:

```sql
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE VOLUME IF NOT EXISTS main.default.vendas_etl;
```

Isso cria o caminho `/Volumes/main/default/vendas_etl/`.

### 2. Subir os Parquets

Abra o Catalog Explorer, navegue até `main` → `default` → `vendas_etl` e use o botão de upload (arrastar e soltar arquivos). Crie uma pasta por tabela e mande o respectivo `part-...parquet` para dentro dela:

```
/Volumes/main/default/vendas_etl/silver/vendas/part-00000-....parquet
/Volumes/main/default/vendas_etl/gold/dim_cliente/part-00000-....parquet
/Volumes/main/default/vendas_etl/gold/dim_produto/part-00000-....parquet
/Volumes/main/default/vendas_etl/gold/fato_vendas/part-00000-....parquet
```

O nome exato dos menus varia um pouco entre workspaces. O que importa é o arquivo terminar nesses caminhos.

### 3. Registrar as tabelas

Apontando uma tabela para a pasta, o Databricks passa a ler o Parquet de lá:

```sql
CREATE TABLE IF NOT EXISTS silver.vendas
USING PARQUET
LOCATION '/Volumes/workspace/default/vendas_etl/silver/vendas';

CREATE TABLE IF NOT EXISTS gold.dim_cliente
USING PARQUET
LOCATION '/Volumes/workspace/default/vendas_etl/gold/dim_cliente';

CREATE TABLE IF NOT EXISTS gold.dim_produto
USING PARQUET
LOCATION '/Volumes/workspace/default/vendas_etl/gold/dim_produto';

CREATE TABLE IF NOT EXISTS gold.fato_vendas
USING PARQUET
LOCATION '/Volumes/workspace/default/vendas_etl/gold/fato_vendas';
```

### 4. Conferir

```sql
SELECT COUNT(*) FROM silver.vendas;      -- 23
SELECT COUNT(*) FROM gold.dim_cliente;   -- 23
SELECT COUNT(*) FROM gold.dim_produto;   -- 13
SELECT COUNT(*) FROM gold.fato_vendas;   -- 23
```

Se der os quatro números, as queries em `sql/` rodam direto.

## O que muda no resultado das queries

- **Sem duplicata:** `VEN-0004` e `VEN-0011` deixam de ser contados duas vezes.
- **Data é `date` de verdade:** vem do Parquet, não mais texto.
- **Valores são `double`:** sem o ajuste manual de vírgula.
- **Texto em minúsculas:** o R4 normaliza, então categoria e canal saem como `informática`, `web`.
- **Valores nulos:** a venda sem preço continua com `valor_unitario` nulo, de propósito.

## Reatualizar depois de mexer no ETL

Rode `python etl/run.py` (o `overwrite` regrava o Parquet), suba o `part-...parquet` novo por cima do antigo no volume e recarregue a tabela:

```sql
REFRESH TABLE silver.vendas;
REFRESH TABLE gold.fato_vendas;
```

## Próximo degrau

Hoje esse upload é manual. O passo seguinte é um `etl/publish_databricks.py` que sobe os Parquets e roda o DDL sozinho, usando um Personal Access Token e a REST API do Databricks.
