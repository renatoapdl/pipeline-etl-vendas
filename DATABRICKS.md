# Databricks CE: carregar o resultado do ETL

As queries em `sql/` no Databricks leem as tabelas em Parquet criadas no ETL.

## O que subir

Depois de rodar `python -m etl.run`, cada tabela é uma pasta em `data/` com um ou mais
`part-*.parquet` (mais um `_SUCCESS` e arquivos `.crc`). Suba **todos os `part-*.parquet`** da pasta.

São 13 tabelas: 7 do Silver e 6 do Gold. Na prática, `silver.orders` e `gold.fato_pagamentos`
saem com 2 arquivos `part` cada — suba os dois.

| Tabela no Databricks | Arquivo local |
|---|---|
| `silver.translation` | `data/silver/translation/part-*.parquet` |
| `silver.products` | `data/silver/products/part-*.parquet` |
| `silver.customers` | `data/silver/customers/part-*.parquet` |
| `silver.sellers` | `data/silver/sellers/part-*.parquet` |
| `silver.orders` | `data/silver/orders/part-*.parquet` |
| `silver.items` | `data/silver/items/part-*.parquet` |
| `silver.payments` | `data/silver/payments/part-*.parquet` |
| `gold.dim_cliente` | `data/gold/dim_cliente/part-*.parquet` |
| `gold.dim_vendedor` | `data/gold/dim_vendedor/part-*.parquet` |
| `gold.dim_produto` | `data/gold/dim_produto/part-*.parquet` |
| `gold.dim_data` | `data/gold/dim_data/part-*.parquet` |
| `gold.fato_itens` | `data/gold/fato_itens/part-*.parquet` |
| `gold.fato_pagamentos` | `data/gold/fato_pagamentos/part-*.parquet` |

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

Abra o Catalog Explorer, navegue até `workspace` → `default` → `vendas_etl` e use o botão de upload
(arrastar e soltar arquivos). Crie uma pasta por tabela e mande o respectivo `part-...parquet` para dentro:

```
/Volumes/workspace/default/vendas_etl/silver/translation/part-....parquet
/Volumes/workspace/default/vendas_etl/silver/products/part-....parquet
/Volumes/workspace/default/vendas_etl/silver/customers/part-....parquet
/Volumes/workspace/default/vendas_etl/silver/sellers/part-....parquet
/Volumes/workspace/default/vendas_etl/silver/orders/part-....parquet
/Volumes/workspace/default/vendas_etl/silver/items/part-....parquet
/Volumes/workspace/default/vendas_etl/silver/payments/part-....parquet
/Volumes/workspace/default/vendas_etl/gold/dim_cliente/part-....parquet
/Volumes/workspace/default/vendas_etl/gold/dim_vendedor/part-....parquet
/Volumes/workspace/default/vendas_etl/gold/dim_produto/part-....parquet
/Volumes/workspace/default/vendas_etl/gold/dim_data/part-....parquet
/Volumes/workspace/default/vendas_etl/gold/fato_itens/part-....parquet
/Volumes/workspace/default/vendas_etl/gold/fato_pagamentos/part-....parquet
```

O nome exato dos menus varia um pouco entre workspaces. O que importa é o arquivo terminar nesses caminhos.

### 3. Registrar as tabelas

Apontando uma tabela para a pasta, o Databricks passa a ler o Parquet de lá:

```sql
CREATE OR REPLACE TABLE silver.translation USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/translation/`;

CREATE OR REPLACE TABLE silver.products USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/products/`;

CREATE OR REPLACE TABLE silver.customers USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/customers/`;

CREATE OR REPLACE TABLE silver.sellers USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/sellers/`;

CREATE OR REPLACE TABLE silver.orders USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/orders/`;

CREATE OR REPLACE TABLE silver.items USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/items/`;

CREATE OR REPLACE TABLE silver.payments USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/silver/payments/`;

CREATE OR REPLACE TABLE gold.dim_cliente USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/dim_cliente/`;

CREATE OR REPLACE TABLE gold.dim_vendedor USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/dim_vendedor/`;

CREATE OR REPLACE TABLE gold.dim_produto USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/dim_produto/`;

CREATE OR REPLACE TABLE gold.dim_data USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/dim_data/`;

CREATE OR REPLACE TABLE gold.fato_itens USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/fato_itens/`;

CREATE OR REPLACE TABLE gold.fato_pagamentos USING DELTA AS
SELECT * FROM parquet.`/Volumes/workspace/default/vendas_etl/gold/fato_pagamentos/`;
```

### 4. Conferir

```sql
SELECT COUNT(*) FROM silver.translation;       -- 71
SELECT COUNT(*) FROM silver.products;          -- 32951
SELECT COUNT(*) FROM silver.customers;         -- 99441
SELECT COUNT(*) FROM silver.sellers;           -- 3095
SELECT COUNT(*) FROM silver.orders;            -- 99441
SELECT COUNT(*) FROM silver.items;             -- 112650
SELECT COUNT(*) FROM silver.payments;          -- 103886

SELECT COUNT(*) FROM gold.dim_cliente;         -- 96096
SELECT COUNT(*) FROM gold.dim_vendedor;        -- 3095
SELECT COUNT(*) FROM gold.dim_produto;         -- 32951
SELECT COUNT(*) FROM gold.dim_data;            -- 774
SELECT COUNT(*) FROM gold.fato_itens;          -- 112650
SELECT COUNT(*) FROM gold.fato_pagamentos;     -- 103886
```

Se os números baterem, as queries em `sql/` rodam direto. A `10_reconciliacao_gold_silver.sql`
compara as somas do Gold com as do Silver e deve devolver diferença `0,00` nas três métricas.