# PRD — pipeline-etl-vendas

> Documento de requisitos do case de portfólio. Descreve o que o projeto entrega e por quê, não o passo a passo de uso.

## 1. Resumo

Pipeline ETL em PySpark com arquitetura Medallion sobre o **Brazilian E-Commerce Public Dataset by Olist** (≈100 mil pedidos, 2016–2018). Lê os 9 CSVs originais, preserva o dado bruto em Bronze, limpa e tipa 7 tabelas em Silver, e modela em estrela na Gold (4 dimensões + 2 fatos). O resultado é consultável por SQL no Databricks Community Edition.

O case existe como prova prática para a transição para Engenharia de Dados: mostrar decisões de tratamento, idempotência, modelagem dimensional, quality gate e uso de SQL sobre uma base real.

Os dados são públicos (Kaggle) e ficam em `dados/olist/`, fora do versionamento.

## 2. Problema

Os CSVs da Olist chegam separados por entidade (pedidos, itens, pagamentos, clientes, vendedores, produtos, tradução de categorias, geolocalização e avaliações), com os problemas típicos de uma base real:

- tipos inconsistentes (tudo chega como texto);
- identificadores que parecem iguais e não são (`customer_id` é por pedido; `customer_unique_id` é a pessoa);
- categorias em português, com uma tabela de tradução à parte;
- pedidos sem item ou sem pagamento;
- valores de item+frete que não fecham com o pagamento em alguns pedidos (voucher, juros);
- colunas de nome/descrição com tamanho e medidas em texto.

Sem tratamento, JOINs quebram, contagens inflam e o faturamento sai errado. Quem consome precisa de camadas confiáveis e de um modelo que responda perguntas de negócio.

## 3. Objetivo

Construir um pipeline que preserve o dado bruto, limpe e tipe, modele em estrela e seja consultável por SQL, com execução idempotente, quality gate e testes automatizados.

## 4. Consumidor

Quem avalia o portfólio (recrutador técnico / time de dados), que clona o repo, baixa a base no Kaggle, roda o pipeline e consulta as tabelas no Databricks CE.

## 5. Escopo (V2, atual)

**Em escopo:**

- Ingestão dos 9 CSVs de `dados/olist/` (schema não declarado, tudo como texto).
- Camada Bronze: Parquet como o dado chegou (9 arquivos).
- Camada Silver: 7 tabelas limpas e tipadas (`translation`, `products`, `customers`, `sellers`, `orders`, `items`, `payments`).
- Camada Gold: modelo estrela (`dim_cliente`, `dim_vendedor`, `dim_produto`, `dim_data`, `fato_itens`, `fato_pagamentos`).
- Quality gate que valida Silver e Gold e bloqueia a publicação do Gold em caso de erro.
- 10 queries SQL (01–10) validadas no Databricks CE.
- 22 testes (pytest) data-independent.
- `README.md` e `DATABRICKS.md`.

**Fora de escopo nesta fase:**

- Usar `geolocation` e `order_reviews` no modelo (são ingeridos no Bronze, mas ficam para uma versão futura).
- Orquestração real (Airflow rodando) — fica para a fase seguinte.
- Particionamento, Delta Lake no pipeline, Kubernetes, warehouse, SQLite e fonte via API.

## 6. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF1 | Ler os 9 CSVs de `dados/olist/` com header, UTF-8, delimitador vírgula e `inferSchema=false` (tudo texto). |
| RF2 | Gravar o dado como chegou em `data/bronze/<arquivo>` (Parquet), sem correção. |
| RF3 | Silver `translation` — normalizar `product_category_name` (trim+lower), derivar `categoria_en` e remover duplicatas por categoria. |
| RF4 | Silver `products` — trim em id/categoria, cast das medidas para `integer`, remover colunas de tamanho de nome/descrição e renomear para os nomes do modelo (`fotos_qty`, `peso_g`, `comprimento_cm`, `altura_cm`, `largura_cm`). |
| RF5 | Silver `customers`/`sellers` — trim, cidade em lower, estado em upper, CEP como string. |
| RF6 | Silver `orders` — trim, status em lower e timestamps em `yyyy-MM-dd HH:mm:ss`. |
| RF7 | Silver `items` — trim nos ids, timestamp, `price` e `freight_value` em `decimal(12,2)`. |
| RF8 | Silver `payments` — trim, `payment_sequential`/`payment_installments` como `integer`, tipo em lower e `payment_value` em `decimal(12,2)`. |
| RF9 | Gold `dim_cliente` — uma linha por `customer_unique_id`, com o endereço do pedido mais recente e chave `cod_cliente`. |
| RF10 | Gold `dim_vendedor` (1 por `seller_id`) e `dim_produto` (categoria PT + EN, chave `cod_produto`). |
| RF11 | Gold `dim_data` — calendário do menor ao maior `order_purchase_timestamp`, com `cod_data = yyyyMMdd`, ano/mês/dia/trimestre/dia da semana/fim de semana/ano_mes. |
| RF12 | Gold `fato_itens` — grão `order_id + order_item_id`, FKs `cod_cliente`, `cod_produto`, `cod_vendedor`, `cod_data` e medidas `price`, `freight_value`. |
| RF13 | Gold `fato_pagamentos` — grão `order_id + payment_sequential`, FKs `cod_cliente`, `cod_data` e medidas/atributos `payment_type`, `payment_installments`, `payment_value`. |
| RF14 | Quality gate: Silver (não vazio, grão, nulos obrigatórios) e Gold (grão, FKs, contagens e somas iguais ao Silver) antes de publicar; erro bloqueia a gravação do Gold. |
| RF15 | Reconciliação por pedido (`price+frete` vs `payment_value`) é registrada como AVISO, não como erro, por ser inconsistência da própria base Olist. |
| RF16 | 10 queries SQL (01–10) consultando `silver.*` e `gold.*` no Databricks. |

## 7. Requisitos não-funcionais

- **Idempotência:** gravação com `overwrite` (via diretório temporário + move, por causa do lock do Windows); rodar duas vezes não duplica linhas.
- **Determinismo:** chaves surrogadas por `row_number` com ordenação fixa (`customer_unique_id`, `seller_id`, `product_id`).
- **Integridade dos fatos:** `left join` nas dimensões e `inner join` em `dim_data`; o item não pode sumir e a soma não pode mudar do Silver para o Gold.
- **Legibilidade:** uma função por tabela/transformação; cada decisão explicada no código.
- **Testes:** automatizados com pytest, data-independent (DataFrames pequenos em memória), rodando no CI sem os CSVs/Parquets reais.
- **Desempenho:** roda local em Spark `local[*]`; o pipeline completo e os 22 testes rodam em poucos minutos.
- **Requisitos de máquina:** Python 3.9+ e Java 11+; no Windows, `winutils.exe` (HADOOP_HOME) e `PYSPARK_PYTHON` apontando para o Python do venv.
- **Encoding:** UTF-8.

## 8. Modelo de dados (Gold, estrela)

- **`dim_cliente`** (`cod_cliente`, `customer_unique_id`, `cidade`, `estado`, `cep_prefixo`) — grão: uma pessoa.
- **`dim_vendedor`** (`cod_vendedor`, `seller_id`, `cidade`, `estado`, `cep_prefixo`) — grão: um vendedor.
- **`dim_produto`** (`cod_produto`, `product_id`, `categoria_pt`, `categoria_en`, `peso_g`, `comprimento_cm`, `altura_cm`, `largura_cm`, `fotos_qty`) — grão: um produto.
- **`dim_data`** (`cod_data`, `data`, `ano`, `mes`, `dia`, `trimestre`, `dia_semana`, `eh_fim_de_semana`, `ano_mes`) — grão: um dia.
- **`fato_itens`** (`order_id`, `order_item_id`, `cod_cliente`, `cod_produto`, `cod_vendedor`, `cod_data`, `price`, `freight_value`) — grão: um item de pedido.
- **`fato_pagamentos`** (`order_id`, `payment_sequential`, `cod_cliente`, `cod_data`, `payment_type`, `payment_installments`, `payment_value`) — grão: uma forma de pagamento de um pedido.

Dois fatos, porque item e pagamento têm grãos diferentes (um pedido pode ter vários itens e vários pagamentos). `customer_id` não é chave de cliente: o mesmo cliente aparece em vários pedidos, e o `customer_unique_id` é que identifica a pessoa.

## 9. Fluxo

```
9 CSVs (dados/olist) → bronze → Silver (7 tabelas) → gate Silver → gold (4 dims + 2 fatos, em memória) → gate Gold → publicar Gold → SQL / Databricks CE
```

## 10. Entregáveis

- `etl/` — `bronze.py` (74), `silver.py` (147), `gold.py` (217), `quality.py` (198), `run.py` (53), `load.py` (50), `sessao.py` (17); 756 linhas no total, sem testes.
- `tests/` — `conftest.py` (24), `test_silver.py` (168), `test_gold.py` (179), `test_quality.py` (164); 22 testes.
- `sql/01` a `sql/10`.
- `README.md`, `DATABRICKS.md`.
- Prints do ETL, do quality gate e das queries no Databricks.

## 11. Critérios de aceite (V2)

- [ ] `python -m etl.run` roda sem erro e termina com "ETL Olist concluido com sucesso".
- [ ] Silver: `translation` 71, `products` 32951, `customers` 99441, `sellers` 3095, `orders` 99441, `items` 112650, `payments` 103886.
- [ ] Gold: `dim_cliente` 96096, `dim_vendedor` 3095, `dim_produto` 32951, `dim_data` 774, `fato_itens` 112650, `fato_pagamentos` 103886.
- [ ] Somas preservadas: `price` 13.591.643,70; `freight_value` 2.251.909,54; `payment_value` 16.008.872,12.
- [ ] `python -m pytest tests -q` com 22 testes passando.
- [ ] Com uma chave duplicada/obrigatória nula no Silver, o gate bloqueia e o Gold não é publicado (código de saída 1).
- [ ] A reconciliação por pedido é exibida como AVISO (303 pedidos divergentes na base Olist) sem bloquear.
- [ ] No Databricks CE, os 13 `count(*)` batem e as 10 queries rodam.
- [ ] A `10_reconciliacao_gold_silver.sql` devolve diferença `0,00` nas três métricas.

## 12. Versões

- **V1 (anterior):** ETL sobre um CSV sintético de vendas, com sujeira proposital.
- **V2 (atual):** base real Olist, Medallion, 7 tabelas Silver, estrela com 2 fatos, quality gate com bloqueio, 22 testes e 10 queries.
- **V3 (depois):** Airflow rodando de verdade, particionamento, Delta no pipeline, uso de geolocalização/avaliações.

## 13. Riscos e decisões abertas

- **Reconciliação:** 303 pedidos têm `price+frete` diferente de `payment_value` por inconsistência da base (vouchers/juros). Tratado como AVISO; os checks de preservação de soma (Gold == Silver) é que são bloqueantes.
- **Airflow:** nesta fase só o conceito (DAG); rodar de verdade fica para a fase seguinte, num sandbox Linux.
- **Windows:** lock de arquivo do Spark exige gravação em temp + move; `PYSPARK_PYTHON` e `winutils.exe` são pré-requisitos.
- **Decimal:** `price`, `freight_value` e `payment_value` usam `decimal(12,2)` para não acumular erro de ponto flutuante nas somas.

## 14. Documentos relacionados

- `README.md` — como rodar e o que o pipeline faz.
- `DATABRICKS.md` — carga das 13 tabelas no Databricks CE.
- `sql/` — as 10 queries.
