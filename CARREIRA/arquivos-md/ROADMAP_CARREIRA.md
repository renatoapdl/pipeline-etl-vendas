# ROADMAP DE CARREIRA — Francisco Renato Holanda de Abreu

> **Documento de Orientação Estratégica** para a transição de carreira, foco único em **Engenharia de Dados**.
> Última atualização: Outubro de 2026 (v3.1 — datas do bootcamp atualizadas para 03/11 a 31/12/2026)

---

## SUMÁRIO EXECUTIVO

**Situação Atual:** Engenheiro Eletricista com 14+ anos em infraestrutura crítica NASA/Mackenzie (Rádio Observatório Espacial do Nordeste — rede IVS-NASA), com experiência real em monitoramento de telemetria, dashboards de performance (Grafana, MTTR, SLA) e automação de dados com Python. Já construiu pipeline ETL em PySpark validado (case `pipeline-etl-vendas`).

**Decisão estratégica (setembro 2026):** foco em **uma única área — Engenharia de Dados** — em nível de **entrada (Júnior)**, em **português**, com o storytelling "engenheiro de confiabilidade NASA migrando para dados". Perfil antigo "Full-Stack / Automação / Web / IA" foi removido do posicionamento.

**Objetivo Final:** Ocupar uma vaga Júnior de Engenharia de Dados, convertendo 14 anos de confiabilidade de sistemas críticos em diferencial de **qualidade de dados, monitoramento e pipeline**.

---

## PARTE 1 — POSICIONAMENTO V3 (feito em 28/set/2026; título ajustado a partir do `CURRICULO_ATS.md`)

### 1.1 Título do LinkedIn (novo)

```
Engenheiro de Dados | Python, PySpark, SQL | 14+ anos em infraestrutura crítica NASA
```

- Remove "em transição", "Full-Stack", "Desenvolvedor", "IoT", "Gestão de Ativos" do headline.
- Contato inclui Landing Page: `renatoapdl.github.io/renato/`.
- O URL `linkedin.com/in/renatoabreuengenharia` permanece (não é autoalterável).

### 1.2 Bio resumo (novo)

"14 anos garantindo a confiabilidade de sistemas de missão crítica da NASA. Em transição para Engenharia de Dados, aplico a mesma mentalidade ao ciclo de dados: pipelines ETL com Python e PySpark, SQL e qualidade de dados. Busco oportunidade de entrada em Engenharia de Dados."

### 1.3 Currículo v3 (arquivos `CURRICULO_ATS.md` e `CURRICULO_PDF.md`)

- **Cabeçalho:** "Engenheiro de Dados | Python, PySpark, SQL | 14+ anos em infraestrutura crítica NASA".
- **Experiência NASA recontada como dados:** dashboards (Grafana, MTTR -35%), automação Python (tempo manual -40%), telemetria, 99.7% de disponibilidade.
- **Projetos:** `pipeline-etl-vendas` em primeiro lugar; depois `clima-eusebio` e `fgo-data-update`.
- **Competências:** Engenharia de Dados (ETL, PySpark, Parquet, data quality, camadas bronze/prata/ouro), SQL, Grafana, Python, Git.

### 1.4 Regras do posicionamento

1. Tudo que não for dados sai dos destaques (web, IoT, ML, IA generativa, automação industrial em geral).
2. Título de vaga-alvo: **Engenheiro de Dados Júnior / Analista de Dados** (em ordem de preferência).
3. Idioma de todos os documentos: **PT-BR** (tradução EN somente após garantir base).
4. Nível: **entrada** — a senioridade de confiabilidade aparece no conteúdo (posts/cases), não no cargo. O cabeçalho não sinaliza "Júnior" nem "em transição".

---

## PARTE 2 — BASE TÉCNICA (requisitos da vaga Banco Mercantil/Domo)

Fonte: `candidaturas\roadmap_vaga.md` e `candidaturas\VAGA_DOMO-MERCANTIL.md`.

| Requisito da vaga | Status | Onde atacar |
|---|---|---|
| PySpark / Spark DataFrames | Quase pronto | Case `pipeline-etl-vendas` + Databricks CE |
| SQL analítico (window functions) | Em desenvolvimento (prioridade até 02/11) | SQLBolt → SQLZoo → LeetCode |
| ETL e Data Quality | V1 pronto; falta quality gate com bloqueio | Semana 4 do plano de preparo |
| Airflow (orquestração) | Não (V2) | Conceito + DAG do case (imagem) na semana 5 |
| Kubernetes (dias a dia) | Não (V2) | Killercoda, 1 tarde na semana 5 |
| Databricks | **Feito** (`case-tratamento-input` rodou no Free/serverless) | Manter; print no README do case |
| Governança IFRS 9 / Basel | Não (V2) | 1 semana de estudos |
| Arquitetura medallion | Decisão: **V2** | bronze/prata/ouro no case |
| SQLite | V3 | persistência/dashboard |
| Consumo de API | Depois | fonte extra do case |

Regra da V1 (dica do amigo): **simples, mas com PySpark. Sem orquestração por enquanto.** O DAG de exemplo é só a imagem da lógica — não precisa de Docker.

---

## PARTE 3 — CURSO DE BASE SÓLIDA (decisão 28/set/2026)

Prioridade de ações:

1. **FEITO em 28/09/2026 — inscrito no Santander Open Academy "Dados com Python e IA" (DIO)** — **R$0**, 15 mil bolsas, 50h, mentorias e certificado. Inscritos têm acesso imediato à "Aceleração Santander" (RAG). Cronograma confirmado em 01/10/2026: inscrições até 14/10, chamadas 16/10, 24/10 e 30/10, bootcamp de **03/11 a 31/12/2026**. Janela de preparo: 01/10 a 02/11 (5 semanas). Atenção: o bootcamp é de Python e IA, não de PySpark/Airflow — não deve virar o eixo do posicionamento, só o certificado.
2. **R$27–90 (Udemy, só em promoção):** "Formação Engenharia de Dados: Domine Big Data" (4.7★, 4,4 mil avaliações) — mais completo; ou "Engenharia de Dados com Python" (4.9★, ETL Pandas + bancos); ou "Data Lake do Zero" (4.7★, PySpark + Airflow + Databricks — bate direto com o case).
3. **R$0 (matriculado, prioridade baixa):** Accenture - Python para Análise e Automação de Dados (55h, DIO). Fundamental de Python e ML; entra em "em tempo livre", não no plano até 02/11. Ver `METAS_CHECKLIST.md` 4.7.
4. **R$0 (prática):** SQLBolt (JOIN, NULL, GROUP BY/HAVING, ordem de execução) → SQLZoo → LeetCode (SQL); docs do PySpark; Databricks CE; docs do Airflow. Roteiro em `aula_sqlbolt.md`.
5. **Acima do teto, só se houver auxílio financeiro:** IBM Data Engineering (Coursera, ~US$49/mês) — o mais reconhecido para a função; grátis quando aprovado auxílio.

Nunca pagar preço cheio da Udemy (preço real = promoção). Detalhar preços/links na consulta original desta sessão.

### 3.1 Ordem de prioridade até 02/11/2026 (definida em 01/10/2026)

| Semana | Foco | Entrega |
|---|---|---|
| 1 (01 a 05/10) | SQL base: SQLBolt (aulas 6, 7, 8 concluídas em 05/10) → SQLZoo → (10–12 pendentes) | pasta `sql/` no case, cada query com a pergunta de negócio que responde |
| 2 (05 a 11/10) | Window function no CSV do case: `row_number`, `lag`, `sum over`, `rank` + esquema estrela (2 dimensões, 1 fato) | 4 queries comentadas |
| 3 (12 a 18/10) | Case V2: medallion (bronze/prata/ouro) | README atualizado + print novo |
| 4 (19 a 25/10) | Case V2: quality gate que **reprova** a publicação + 2 testes | commit + resposta para "como você garante qualidade em produção?" |
| 5 (26/10 a 02/11) | Arredondar: conceito de Airflow (DAG impressa), K8s no Killercoda 1 tarde, subir no Databricks CE | print do Databricks no README |
| 5b (paralelo) | Sandbox Linux na máquina da sua rede, para rodar o Airflow de verdade (Docker) | `docker-compose.yml` com Postgres + Airflow no ar |

SQL antes de PySpark porque o checklist ainda tem JOIN/GROUP BY/CTE/window em aberto e o case não tem SQL; PySpark window já está demonstrado no pipeline. Fora do caminho agora: K8s profundo, Snowflake, MLOps, IFRS 9/Basel, SQLite, API, Udemy.

---

## PARTE 4 — PORTFÓLIO E GITHUB

### 4.1 Repositórios (foco em dados)

| Repositório | Papel | Ação |
|---|---|---|
| `pipeline-etl-vendas` | **Protagonista** | Subir no GitHub (git init + commits lógicos) e criar README completo |
| `case-tratamento-input` | **Case Databricks (FEITO 30/09/2026)** | Publicado com README, notebook e auditoria documentada |
| `clima-eusebio` | Dados em tempo real (API) | Manter como está (README ok) |
| `fgo-data-update` | Dados NASA (VLBI) | Criar README (case NASA) |
| `BAIXADOR-X` | Secundário | Mantém, fora dos destaques |
| `renato` / `renatoapdl` | Extras | Sem urgência |

### 4.2 Evolução do case `pipeline-etl-vendas`

- **V1 (pronta):** ETL PySpark simples, 27 → 25 → 23 registros válidos, Parquet bruto/tratado, 9 testes.
- **V2:** medallion (bronze/prata/ouro) + base real do amigo (CSV/Parquet) + Airflow (DAG impresso) + rodar no Databricks CE.
- **V3:** SQLite para consultas/dashboard + fonte via API.

---

## PARTE 5 — LINKEDIN: PLANO DE CONTEÚDO (dados)

**Frequência:** 1 post/semana.

**Gatilho de tema (≠ vagas genéricas):**

1. "Das telemetrias da NASA ao pipeline ETL" (case pipeline-etl-vendas)
2. "MTTR, SLA e qualidade de dados: por que confiabilidade é data engineering"
3. "Do rádio telescópio ao PySpark: minha transição"
4. "O que aprendi quebrando um pipeline de vendas (27 → 25 → 23)"
5. "Por que comecei pela camada bruta antes de falar de dashboards"
6. "SQL de verdade: 100 dias de LeetCode saindo da manutenção"

**Regras:** responder todos os comentários nas primeiras 2h; postar terça–quinta, 8h–10h ou 18h–20h; usar os rascunhos de `POST_LINKEDIN_v1.md` (já ajustados para dados).

---

## PARTE 6 — CRONOGRAMA (comprimido: ~6 meses até começar a candidatura)

| Período | Foco | Entregáveis |
|---|---|---|
| Dias 1–7 | Posicionamento no ar + Santander | Título/bio/currículo v3 publicados; **inscrito no Santander (28/09; início 03/11, fim 31/12)**; `pipeline-etl-vendas` no GitHub com README. Preparação até 02/11: SQL semanal + case V2 (medallion na semana 3, quality gate na semana 4) |
| Mês 1–2 | PySpark + Databricks CE + SQL | Case V2 no GitHub (medallion + base real); SQL diário no LeetCode |
| Mês 3–4 | Orquestração + nuvem + governança | Airflow (DAG do case), Databricks CE rodando, IFRS9/Basel ~1 semana |
| Mês 5–6 | Candidaturas ativas + entrevistas | LinkedIn aquecido (12+ posts); candidaturas semanais; prática de entrevista com o case |
| Contínuo | Curso da Parte 3 + posts semanais | Certificado Santander (+ opcional 1 Udemy em promoção) |

---

## PARTE 7 — MÉTRICAS

| Métrica | Meta |
|---|---|
| Case no GitHub com README | 1 (pipeline-etl-vendas) |
| Repos com README completo | 4 (pipeline-etl-vendas, clima-eusebio, fgo-data-update, BAIXADOR-X) |
| Posts no LinkedIn | 12 em 6 meses (1/semana) |
| Conquistas no LinkedIn | Projetos (3), Certificados (2 em andamento) |
| LeetCode SQL | 200 problemas em 6 meses |
| Candidaturas ativas | 20+ a partir do mês 5 |

---

## PARTE 8 — MENSAGENS FINAIS

**Seu diferencial competitivo:** 14 anos de sistemas de missão crítica (raro), rede NASA (abre portas), mentalidade de confiabilidade (KPIs/SLAs/OEE — o que falta em 90% dos dados), experiência real com telemetria/sensores (não se aprende em curso), inglês técnico.

> A transição não é sobre apagar o passado e recomeçar. É sobre **conectar** o que você já sabe com o que quer aprender. Telemetria, dashboards, automação, confiabilidade — tudo isso é **experiência com dados**. O case PySpark só prova o que você já viveu 14 anos: dados precisam ser confiáveis.

---

*Documento v3 gerado em Setembro de 2026. Atualizar trimestralmente.*