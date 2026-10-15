# Databricks CE: carregar o resultado do ETL

As queries em `sql/` no Databricks lêem as tabelas em Parquet criadas no ETL 

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
CREATE VOLUME IF NOT EXISTS workspace.default.vendas_etl;
```

Isso cria o caminho `/Volumes/workspace/default/vendas_etl/`.

### 2. Subir os Parquets

Abra o Catalog Explorer, navegue até `workspace` → `default` → `vendas_etl` e use o botão de upload (arrastar e soltar arquivos). Crie uma pasta por tabela e mande o respectivo `part-...parquet` para dentro dela:

```
/Volumes/workspace/default/vendas_etl/silver/vendas/part-00000-....parquet
/Volumes/workspace/default/vendas_etl/gold/dim_cliente/part-00000-....parquet
/Volumes/workspace/default/vendas_etl/gold/dim_produto/part-00000-....parquet
/Volumes/workspace/default/vendas_etl/gold/fato_vendas/part-00000-....parquet
```

O nome exato dos menus varia um pouco entre workspaces. O que importa é o arquivo terminar nesses caminhos.

### 3. Registrar as tabelas

Apontando uma tabela para a pasta, o Databricks passa a ler o Parquet de lá:

```sql
CREATE OR REPLACE TABLE silver.vendas USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/vendas/`;

CREATE OR REPLACE TABLE gold.dim_cliente USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/dim_cliente/`;

CREATE OR REPLACE TABLE gold.dim_produto USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/dim_produto/`;

CREATE OR REPLACE TABLE gold.fato_vendas USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/fato_vendas/`;
```

### 4. Conferir

```sql
SELECT COUNT(*) FROM silver.vendas;      -- 23
SELECT COUNT(*) FROM gold.dim_cliente;   -- 23
SELECT COUNT(*) FROM gold.dim_produto;   -- 13
SELECT COUNT(*) FROM gold.fato_vendas;   -- 23
```

Se der os quatro números, as queries em `sql/` rodam direto.