# PRD — pipeline-etl-vendas

> Documento de requisitos do case de portfólio. Descreve o que o projeto entrega e por quê, não o passo a passo de uso.

## 1. Resumo

Pipeline ETL em PySpark com arquitetura Medallion. Lê um CSV de vendas sujo, preserva o dado bruto em Bronze, limpa e tipa em Silver, e modela em estrela na Gold. O resultado é consultável por SQL no Databricks Community Edition.

O case existe como prova prática para a transição para Engenharia de Dados: mostrar decisões de tratamento, idempotência, modelagem e uso de SQL sobre dados reais.

Os dados são sintéticos e versionados em `dados/vendas_bruto.csv`, com sujeira proposital: cada regra do pipeline tem um motivo concreto no arquivo.

## 2. Problema

Dados de vendas chegam num único CSV, com sujeira parecida com a do mundo real:

- valores em dois formatos (`189,90` e `R$ 1.234,56`);
- datas em dois padrões (`dd/MM/yyyy` e `yyyy-MM-dd`);
- texto com caixa e espaço sobrando (`  Notebook  `, `CABO USB`);
- duplicatas (`VEN-0004`, `VEN-0011`);
- campos vazios (quantidade, situação, preço).

Sem tratamento, agrupar por categoria/canal quebra e o faturamento sai errado. Quem consome precisa de camadas confiáveis e de um modelo que responda perguntas de negócio.

## 3. Objetivo

Construir um pipeline que preserve o dado bruto, limpe e tipe, modele em estrela e seja consultável por SQL, com execução idempotente e testes automatizados.

## 4. Consumidor

Quem avalia o portfólio (recrutador técnico / time de dados), que clona o repo, roda o pipeline e consulta as tabelas no Databricks CE.

## 5. Escopo (V2, atual)

**Em escopo:**

- Ingestão do CSV com schema declarado (tudo como `string`).
- Camada Bronze: Parquet como o dado chegou.
- Camada Silver: regras R1–R6 + D1 (campo derivado).
- Camada Gold: modelo estrela (`dim_cliente`, `dim_produto`, `fato_vendas`).
- 10 queries SQL (01–10) validadas no Databricks CE.
- Quality gate que reprova a publicação (Silver e Gold).
- 11 testes (pytest).
- `README.md` e `DATABRICKS.md`.

**Fora de escopo nesta fase (por decisão):**

- Orquestração real (Airflow rodando).
- Particionamento, Delta Lake no pipeline, Kubernetes, warehouse, SQLite e fonte via API (V3/depois).

## 6. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF1 | Ler `dados/vendas_bruto.csv` com header, UTF-8 e schema declarado (todas as colunas como `string`). |
| RF2 | Gravar o dado como chegou em `data/bronze/vendas` (Parquet). |
| RF3 | R1 — descartar registros sem `id_venda` ou sem `data_venda`. |
| RF4 | R2 — padronizar datas (`dd/MM/yyyy` e `yyyy-MM-dd`) para `date`. |
| RF5 | R3 — converter `valor_unitario` (`R$`, ponto de milhar, vírgula) para `double`. |
| RF6 | R4 — normalizar texto (`trim` + `lower`) em produto, categoria, canal e situação. |
| RF7 | R5 — preencher nulos: `quantidade` vazia vira 1; `situacao` vazia vira `desconhecida`. Preço vazio continua nulo. |
| RF8 | R6 — remover duplicatas por `id_venda`, mantendo a data mais recente. |
| RF9 | D1 — criar `valor_total = round(quantidade * valor_unitario, 2)`. |
| RF10 | Gravar Silver em `data/silver/vendas`. |
| RF11 | Gerar a estrela: `dim_cliente(id_cliente, cod_cliente)`, `dim_produto(cod_produto, produto, categoria)`, `fato_vendas(id_venda, data_venda, cod_cliente, cod_produto, canal, quantidade, valor_unitario, valor_total)`. |
| RF12 | Mostrar no log o efeito de cada regra (contagem antes → depois) e avisar (`ATENCAO`) sem abortar. |
| RF13 | 10 queries SQL (01–10) consultando `silver.vendas` e as tabelas da Gold no Databricks. |
| RF14 | Quality gate: validar o Silver (id, data, cliente, produto, categoria, quantidade e preço) e o Gold (contagem do fato e chaves) antes de publicar; erro bloqueia a gravação do Gold. |

## 7. Requisitos não-funcionais

- **Idempotência:** gravação com `overwrite`; rodar duas vezes não duplica linhas.
- **Determinismo:** chaves surrogadas por `row_number` com ordenação fixa; duplicata resolvida por regra determinística.
- **Integridade do fato:** `left join` nas dimensões; venda sem correspondência fica com código nulo (sinal de dado ruim) em vez de sumir.
- **Legibilidade:** uma função por regra; cada decisão explicada no código.
- **Testes:** automatizados com pytest, um por regra, os casos de borda e o quality gate.
- **Desempenho:** roda local em cerca de 15 segundos.
- **Requisitos de máquina:** Python 3.9+ e Java 11+.
- **Encoding:** UTF-8.

## 8. Modelo de dados (Gold, estrela)

Grão do fato: uma linha por venda (`id_venda`).

- `dim_cliente`: `id_cliente` (natural) + `cod_cliente` (surrogada).
- `dim_produto`: `produto` + `categoria` → `cod_produto`.
- `fato_vendas`: medidas (`quantidade`, `valor_unitario`, `valor_total`) + chaves (`cod_cliente`, `cod_produto`).
- A `categoria` é atributo do produto: se virasse dimensão à parte, seria snowflake.

## 9. Fluxo

```
CSV → extract → Bronze → transform (R1–R6 + D1) → Silver → quality gate → gold (estrela) → Gold → SQL / Databricks CE
```

## 10. Entregáveis

- `etl/` (extract 40, transform 61, load 19, gold 73, quality 133, run 85 linhas; 411 no total, sem testes).
- `tests/test_transform.py` (9 testes) e `tests/test_quality.py` (2 testes).
- `sql/01` a `sql/10`.
- `README.md`, `DATABRICKS.md`.
- Prints das queries no Databricks.

## 11. Critérios de aceite (V2)

- [ ] `python etl/run.py` roda sem erro e termina com "ETL (Medallion) concluido com sucesso".
- [ ] Bronze 27 linhas, Silver 23; log com R1 `27 → 25` e R6 `25 → 23`.
- [ ] Gold: `fato_vendas` 23, `dim_cliente` 23, `dim_produto` 13; nenhuma chave nula.
- [ ] `python -m pytest tests -q` com 11 testes passando.
- [ ] Com uma data inválida no CSV, o pipeline sai com código 1 e não grava o Gold.
- [ ] No Databricks CE, os 4 `count(*)` batem e as 10 queries rodam.
- [ ] As queries 09 e 10 reconciliam com as 01 e 03.

## 12. Versões

- **V1 (pronta):** ETL PySpark simples, Parquet bruto/tratado, 9 testes.
- **V2 (atual):** Medallion + modelo estrela + SQL no Databricks CE + quality gate com bloqueio (11 testes).
- **V3 (depois):** SQLite para consultas, fonte via API, particionamento, Delta no pipeline, Airflow rodando de verdade.

## 13. Riscos e decisões abertas

- **Airflow:** nesta fase só o conceito (DAG impressa). Rodar de verdade fica num sandbox Linux (Docker + WSL2, Astro CLI já instalados na máquina).
- **Quality gate:** implementado em `etl/quality.py`; o Silver é validado antes de gerar o Gold e erros bloqueiam a publicação (código de saída 1).

## 14. Documentos relacionados

- `README.md` — como rodar e o que o pipeline faz.
- `DATABRICKS.md` — carga das tabelas no Databricks CE.
- `sql/` — as 10 queries.
