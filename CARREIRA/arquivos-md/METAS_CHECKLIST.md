# CHECKLIST DE METAS — Carreira (Engenharia de Dados)

> Controle de progresso das metas definidas no Roadmap de Carreira (v3 — foco único em Engenharia de Dados).
> **Legenda:** `[ ]` Pendente | `[x]` Concluído | `[-]` Em andamento

---

## 1. LINKEDIN

### 1.1 Perfil (v3 — posicionamento em dados)
- [x] Atualizar título do perfil: "Engenheiro de Dados | Python, PySpark, SQL 
- [x] Reescrever bio/narrativa de transição (foco em dados)
- [x] Adicionar Landing Page (renatoapdl.github.io/renato/) ao contato
- [x] Declarar Tech Stack de dados (PySpark, SQL, Pandas, Grafana, Parquet)
- [x] Reorganizar experiência profissional (NASA recontada como dados)
- [x] Adicionar projetos orientados a dados (pipeline-etl-vendas no topo)
- [x] Manter skills SQL, Grafana, Git, APIs REST
- [x] Subir case `pipeline-etl-vendas` no GitHub (vira o primeiro link de projetos)

### 1.2 Conteúdo & Networking
- [-] Criar 1 post por semana sobre dados/transição (12 em 6 meses)
- [-] Conectar com profissionais de dados/engenharia de dados no Brasil
- [-] Seguir empresas-alvo e interagir com conteúdo
- [ ] Meta de seguidores: +50 (6 meses) / +150 (12 meses)

---

## 2. GITHUB

### 2.1 Repositórios
- [x] Realizar git init + commits lógicos do `pipeline-etl-vendas`
- [x] Ter 5 repos limpos e com propósito (4 de cursos deletados)
- [x] Criar README profissional do `pipeline-etl-vendas` (arquitetura, como rodar, testes)
- [ ] Criar README do `fgo-data-update` (case NASA)
- [x] README dos repos menores OK (clima-eusebio, BAIXADOR-X já prontos)

### 2.2 Projetos de dados (em ordem de prioridade)

#### Fase 1 — Case PySpark (protagonista)
- [x] `pipeline-etl-vendas` no GitHub com README completo
- [x] **Case Databricks concluído (30/09/2026):** 13 regras, 1 query única, auditoria coluna a coluna — `case-tratamento-input`
- [x] V2 do case: rodar no Databricks Community Edition (validado no Free/serverless)
- [ ] V2 do case: medallion (bronze/prata/ouro) — semana 3
- [ ] V2 do case: quality gate que reprova a publicação + 2 testes — semana 4
- [ ] V2 do case: DAG Airflow impresso (lógica documentada) — semana 5
- [ ] Base real (CSV/Parquet) integrada ao case

#### Fase 2 — Fundamentos (base da vaga)
- [ ] SQL avançado: 200 problemas no LeetCode (window functions, JOINs)
- [ ] PySpark avançado: window, joins, otimização
- [ ] Airflow: conceito + DAG do case
- [ ] Kubernetes: conceitos básicos (killercoda)
- [ ] Governança: IFRS 9 / Basel (1 semana)

#### Fase 3 — Evoluções (depois)
- [ ] V3 do case: SQLite para consultas
- [ ] V3 do case: fonte via API

#### Fora do caminho crítico (opcional)
- [ ] ML/Scikit-learn (fica depois da primeira vaga)
- [ ] IA Generativa/LangChain (fica depois da primeira vaga)
- [ ] Portfolio HTML (fica depois da primeira vaga)

---

## 3. CURRÍCULO

### 3.1 Estrutura (v3 — Eng. de Dados)
- [x] Reescrever resumo profissional conectando NASA + dados
- [x] Adicionar métricas quantificáveis em cada bullet point
- [x] Incluir projeto `pipeline-etl-vendas` como protagonista
- [x] Atualizar seção "Projetos Relevantes" com links GitHub
- [x] Atualizar versão ATS (texto puro) — `CURRICULO_ATS.md`
- [x] Atualizar versão visual — `CURRICULO_PDF.md`
- [ ] Traduzir para inglês (vagas internacionais, depois da base)
- [x] Alinhar o currículo com o novo título do LinkedIn (feito na v3)

---

## 4. ESTUDOS & CERTIFICAÇÕES

### 4.1 Curso base (decisão 28/set/2026)
- [x] **Inscrito em 28/09/2026:** Santander Open Academy "Dados com Python e IA" (DIO) — R$0. Cronograma confirmado em 01/10/2026: inscrições até 14/10, chamadas 16/10, 24/10 e 30/10, bootcamp de **03/11 a 31/12/2026**
- [ ] Concluir Santander (~50h, com certificado)
- [ ] Aproveitar acesso imediato à "Aceleração Santander" (RAG · ChromaDB/LlamaIndex)
- [ ] Opcional: 1 curso Udemy em promoção (R$27–90) — Formação Eng. de Dados / Data Lake do Zero
- [ ] Opcional: IBM Data Engineering (Coursera)

### 4.1b Preparação até 02/11 (5 semanas · 01/10 → 02/11)
- [x] Reescrever `etl/transform.py` à mão do zero (7 regras R1–R6 + D1) — concluído 05/10/2026
- [x] SQL: SQLBolt aulas 6–8 concluídas em 05/10/2026
- [ ] SQL: SQLBolt → SQLZoo → window functions (semana 2, focar aulas 10–12)
- [ ] Medallion bronze/prata/ouro no case (semana 3)
- [ ] Quality gate que reprova a publicação + 2 testes (semana 4)
- [ ] Airflow só o conceito (DAG impressa) e K8s no Killercoda 1 tarde (semana 5)
- [ ] 1 desafio LeetCode/DIO de SQL por semana

### 4.2 SQL (70% do dia a dia de dados)
- [x] SELECT, WHERE, ORDER BY, LIMIT
- [x] JOINs (INNER, LEFT, RIGHT, FULL) — concluído 05/10/2026 (SQLBolt 6–7)
- [x] NULL — concluído 05/10/2026 (SQLBolt 8)
- [ ] GROUP BY, HAVING, funções de agregação — semana 1 (SQLBolt 10–11)
- [ ] Subqueries e CTEs — semana 2
- [ ] Window functions (ROW_NUMBER, RANK, LAG/LEAD, SUM OVER) — semana 2, prioridade máxima
- [ ] Modelagem simples (criação de tabelas, índices, views)

### 4.3 PySpark / Spark
- [x] Spark DataFrames, colunas, conditions (case pronto)
- [x] Leitura/escrita CSV e Parquet (case pronto)
- [x] Agregações e sumarizações (case pronto)
- [ ] Window functions em PySpark
- [ ] Otimização (partições, broadcast, cache)
- [x] Rodar em Databricks CE (case `case-tratamento-input`, Free/serverless)

### 4.4 ETL / Pipelines
- [x] ETL V1 com validação e data quality (case)
- [ ] Medallion (bronze/prata/ouro) — V2
- [ ] Airflow: conceito, DAG, agendamento — V2
- [ ] Integrar base real do amigo — V2

### 4.5 Ferramentas de dados
- [x] Grafana (dashboards operacionais na NASA)
- [x] Databricks SQL (case de tratamento — Free Edition serverless)
- [ ] Parquet/Delta (formato do case)
- [ ] Understand de governança (IFRS 9/Basel) — V2
- [ ] Container/Kubernetes básico — V2
- [x] **Linux no dia a dia:** Debian em 4+ máquinas reais de produção (acesso via MobaXterm/SSH), redes e telemetria IVS-NASA. Confirmado em 01/10/2026. **Não é lacuna, é diferencial** (ver `VAGA_DOMO-MERCANTIL.md`, onde já está marcado como tal)
- [ ] When usar Linux de verdade: máquina real na rede, não WSL. Servidor próprio como sandbox para o Docker do Airflow (semana 5)

### 4.6 Certificações
- [x] Cybersecurity and Privacy Awareness Training — NASA ✅
- [ ] Grafana: treinamento/certificação (ferramenta do dia a dia)
- [ ] Certificado do Santander "Dados com Python e IA"

---

### 4.7 Cursos extras (matriculados, prioridade baixa, em tempo livre)
- [x] **Matriculado em 01/10/2026 (sugerido pela DIO):** Accenture - Python para Análise e Automação de Dados — 55h, gratuito, 10 módulos, 3 desafios, certificado DIO. Grade: Onboarding + IA; Python para análise; manipulação de dados; POO aplicada; fundamentos de banco e SQL; bibliotecas essenciais (pandas); automação e visualização; fundamentos de ML; desafio final (assistente com IA generativa).
- **Prioridade BAIXA. Não entra no plano de 01/10 a 02/11.** Motivos: módulos 2 a 7 são fundamentals de Python que a experiência NASA já cobre; módulo 8 é ML, que o roadmap joga para depois da primeira vaga; módulo 9 é projeto de IA generativa, barrado pela regra 1 do posicionamento. Só o módulo 5 (SQL) serve de referência, e o SQLBolt já cobre o gap com material melhor.
- [ ] Fazer apenas o módulo 1 (Onboarding, ~2h), quando sobrar tempo
- [ ] Cadastrar o perfil no **Talent Match** da DIO (valor real, custo zero de estudo)
- [ ] Reavaliar em janeiro/2027, depois do bootcamp Santander

---

## 5. CHECKLIST SEMANAL

- [-] Estudar 5x por semana (mínimo 1h/dia)
- [-] Commitar código no GitHub pelo menos 3x por semana (case evoluindo)
- [-] Postar no LinkedIn 1x por semana (tema de dados)
- [ ] Resolver problemas de SQL (LeetCode) 5x por semana
- [-] Conectar com 5 profissionais novos de dados por semana

---

## 6. CRONOGRAMA (~6 meses até começar a candidatura)

| Período | Foco | Status |
|---------|------|--------|
| Dias 1–7 | Posicionamento v3 no ar + Santander + case no GitHub | [-] |
| 01/10 a 02/11 | SQL semanal + case V2 (medallion, quality gate) | [ ] |
| 03/11 a 31/12 | Bootcamp Santander (Python e IA) — não muda o eixo do posicionamento | [ ] |
| Jan a Mar | Candidaturas ativas + entrevistas (20+ candidaturas) | [ ] |
| Contínuo | 1 post/semana + curso Santander | [ ] |

---

*Última atualização: Outubro de 2026 (v3.1 — datas do bootcamp e plano de 5 semanas)*

*Próximos posts no LinkedIn: 08/10 (SQL window functions), 15/10 (medallion), 22/10 (quality gate), 29/10 (retrospectiva do case). Cada post sai de um commit.*