# VAGA — ENGENHEIRO DE DADOS (RISCO DE CRÉDITO) | BANCO MERCANTIL / DOMO

> Arquivo de contexto da candidatura. Tudo que eu (opencode) preciso saber sobre esta vaga está aqui.
> **Status:** `[x] Não candidatei` | `[-] Em andamento` | `[x] Candidatado` | `[x] Recusado`
> **Via de entrada:** indicação de amigo que conversa com a coordenadora do projeto no banco
> **Última atualização:** 25/09/2026

---

## 1. DADOS DA VAGA

| Campo | Informação |
|-------|-----------|
| Empresa | **Banco Mercantil** (Grupo Mercantil) — o **DOMO** é o hub de inovação e tecnologia |
| Marca / hub | DOMO Inovação (`domoinovacao.io`) — *#VEMSERDOMO* |
| Cargo | Engenheiro de Dados |
| Área | Risco de Crédito (dados) |
| Senioridade publicada | Sênior |
| **Senioridade pretendida** | **Júnior / Pleno** — o amigo tenta convencer a coordenadora a abrir o nível |
| Modelo de trabalho | Remoto (vagas do DOMO são 100% remotas) |
| Localização | Brasil (remoto) |
| Tipo de contrato | <!-- preencher: CLT / PJ --> |
| Salário | <!-- valor repassado pelo amigo; a coordenadora vai confirmar a faixa --> |
| Benefícios | plano de saúde e odontológico, Wellhub, vale-transporte, vale-alimentação e refeição, Academia Mercantil, parcerias educacionais, previdência privada, seguro de vida, day off, licenças maternidade/paternidade estendidas |
| Stack visível | AWS, Snowflake, gRPC, Python, SQL, Airflow, Spark, Hadoop, Kubernetes, MLOps |
| Link da vaga | <!-- colar URL --> |
| Data de publicação | <!-- preencher --> |
| Prazo | <!-- preencher --> |

### Contexto da empresa
- Hub de inovação do **Grupo Mercantil**, banco com **80 anos de atuação**, foco em clientes **50+**.
- **Great Place To Work 2025/2026**.
- DNA: "somos intensos na busca por soluções... Precisamos trabalhar em uma esfera profunda de ideias sem restrições."
- Vocabulário oficial das vagas: *Seus principais desafios serão* → *Buscamos uma pessoa com* → *Vai se destacar se apresentar* → *O que oferecemos às pessoas*.
- Cultura de dados citada em outros cargos do DOMO: **governança de dados** (Snowflake como plus), **GenIA/ML**, MLOps.

---

## 2. RESUMO DA VAGA

Posição de Engenharia de Dados dentro da área de **Risco de Crédito** do DOMO (Banco Mercantil). O objetivo é
construir e sustentar a base de dados que alimenta a decisão de crédito do banco: pipelines ETL/ELT que integram
múltiplas fontes, governados pela **Resolução Bacen nº 4.966/21**, com qualidade, disponibilidade e suporte direto
à área de negócio. É a posição que o **amigo tenta rebaixar de Sênior para Pleno/Júnior** para eu entrar.

---

## 3. RESPONSABILIDADES (texto da vaga)

- [ ] Projetar, desenvolver e implementar **pipelines de dados (ETL/ELT)** eficientes e escaláveis para integrar,
      transformar e carregar dados de diversas fontes relevantes para a área de Risco de Crédito
- [ ] Atualizar de forma constante o **Manual de Procedimentos e Política** da área, com alterações em tarefas
      existentes e inclusão de novas atividades
- [ ] Monitorar, manter e otimizar a **infraestrutura de dados** existente para garantir disponibilidade,
      performance e segurança — ajustes e melhorias contínuas
- [ ] Implementar e monitorar processos de **qualidade de dados**: regras de validação, *profiling* e garantia de
      integridade e confiabilidade, alinhado às políticas de **governança de dados** e à **Resolução Bacen nº 4.966/21**
- [ ] Fornecer **suporte técnico** à equipe de Risco de Crédito no acesso e uso dos dados: identificar necessidades,
      resolver problemas e implementar novas soluções de dados

**Leitura da vaga (o que ela realmente pede):** é uma vaga de engenharia de dados de produção com forte componente
de **confiabilidade e conformidade**. Não é vaga de "cientista de dados" — é alguém que constrói, roda, monitora
e **documenta e justifica** o pipeline. É aqui que o meu histórico de engenharia (PCM, SLAs, MTTR, documentação
técnica, ativo crítico) é argumento forte, não uma fraqueza.

---

## 4. REQUISITOS — ANÁLISE ITEM A ITEM

| Requisito | Atende? | Evidência / Onde aparece no currículo | Lacuna real |
|-----------|---------|-------------------------------------|-------------|
| Formação superior completa | `[x]` | Engenharia Elétrica e Eletrônica — UNINTER (2017–2022) + Técnico em Eletrotécnica — CEPEP | Nenhuma. **Este item eliminou o candidato anterior** (ver seção 9.4) |
| SQL | `[~]` | Projeto **FGO Data Update**, uso diário de banco e SAP/ERP | Precisa de SQL analítico (joins, window functions, CTEs) e não só transacional |
| Python | `[x]` | **BAIXADOR-X**, **Clima Eusébio**, scripts de telemetria (Mackenzie/NASA) | Projetos são pequenos; falta projeto com volume e estilo "produção" |
| Big Data — Spark / Hadoop | `[ ]` | — | **Lacuna nº 1** — PySpark é o mais citado em vaga de dados |
| Orquestração — Airflow | `[ ]` | — | **Lacuna nº 2** — conceitualmente é DAG e pipeline, então minha experiência ajuda |
| Kubernetes | `[ ]` | — | **Lacuna nº 3** — uso Linux, VM e servidores remotos, mas não orquestro containers |
| Linux | `[x]` | Infraestrutura crítica NASA, redes, telemetria, Linux no dia a dia | Nenhuma — este é meu diferencial |
| MLOps | `[ ]` | — | **Lacuna nº 4** — tranquilo de aprender, é próximo de DevOps e infra que já fiz |
| Experiência financeira/bancária | `[ ]` | — | **Lacuna nº 5** — a mais crítica para o RH, ver seção 6 |
| Governança de dados / Bacen 4.966/21 | `[ ]` | Política de PCM/PCP e documentação de ativos servindo a área controlada | Precisa aprender vocabulário e lógica de Basel e IFRS 9 |

`[x]` atende · `[~]` parcial · `[ ]` não atende

---

## 5. REQUISITOS DESEJÁVEIS (PLUS)

- [ ] Experiência anterior em segmento financeiro ou bancário
- [ ] Conhecimento em MLOps
- [ ] Experiência com AWS / Snowflake (visível em outras vagas do DOMO)
- [ ] Conhecimento em gRPC

---

## 6. ANÁLISE DE ENCAIXE

**Fit geral (para a vaga Sênior como está publicada):** 2,5 / 5
**Fit (para uma vaga Pleno/Júnior reescopada):** 4 / 5

### Pontos fortes (o que me coloca acima da média)
- **Linux e infra de produção** — 14 anos em infraestrutura crítica com 99,7% de disponibilidade. A vaga pede
  exatamente "disponibilidade, performance e segurança da infraestrutura de dados".
- **Confiabilidade e operação contínua** — o coração da vaga é *monitorar, manter, otimizar*. Sei fazer isso
  (SLA, MTTR, supervisório remoto, análise de falhas).
- **Documentação técnica obrigatória** — a vaga cita *Manual de Procedimentos e Política*. Escrevo procedimento
  técnico em português **e inglês** para a rede IVS-NASA.
- **Comunicação com negócio** — "suporte técnico à equipe de Risco de Crédito" é o que eu já faço: transformo
  dado técnico em algo que o time de negócio consegue usar.
- **Inglês avançado (C1 leitura/escrita)** — raro em candidato de dados, útil em banco.
- **Formação em engenharia com automação industrial** — o currículo é lido como "engenharia de sistemas", não como "curso de dados".
- **Formação superior completa** — pré-requisito que reprovou o candidato anterior.
- **Curiosidade técnica real** — Python fora do trabalho, 3 projetos públicos no GitHub, em transição ativa.

### Lacunas / riscos
- **Sem domínio de crédito/bancário.** Não sei o que é PD, EAD, LGD, provisão IFRS 9, Basel, rating, RWA, PDIF.
- **Sem experiência com a stack de dados moderna em produção** — PySpark, Airflow, Kubernetes, Snowflake.
- **Projetos GitHub pequenos** (scripts e apps desktop) — a vaga pede pipeline escalável. Um projeto de dados
  de verdade é o que mais vai me diferenciar, e é **exatamente o que a coordenadora pediu** (seção 9.3).
- **Sem vivência com ambiente regulado/auditado** — Bacen, auditoria, comitês de risco.
- **Currículo não tem a palavra "dados" no topo** — está posicionado como engenheiro e automação.
- **Risco de senioridade (o meu maior medo, ver 9.3):** aceitar Pleno e não entregar a autonomia esperada.
  Mitigação: não aceitar Pleno sem o projeto case publicado, e negociar rampa explícita de 90 dias.

### Requisitos críticos não atendidos
- **Segmento financeiro/bancário** (é o filtro nº 1 do RH e aparece como "vai se destacar").
- **MLOps**.
- **Spark/Airflow/Kubernetes** (a base técnica da stack).

---

## 7. ESTRATÉGIA DE CANDIDATURA (via indicação)

**Nível a negociar:** aceito **Júnior ou Pleno**, com condição. Se vier Pleno, exijo duas coisas combinadas:
(a) plano de rampa de 90 dias acordado por escrito e (b) o projeto case publicado. Sem os dois, o certo é
aceitar Júnior. O salário de Pleno é maior, mas a cobrança de autonomia também é.

**Ângulo de venda:**
> "Sou engenheiro de operação de infraestrutura crítica com 14 anos garantindo disponibilidade de sistemas que
> não podem cair (99,7%) e construo automação em Python. Estou em transição consolidada para dados, e Risco
> de Crédito é exatamente onde minha mentalidade de confiabilidade, governança e documentação vira vantagem —
> não só onde eu preciso aprender Spark."

**O que o amigo precisa defender para a coordenadora:**
1. Que existe uma **vaga Pleno/Júnior** de verdade, e não apenas um candidato experiente demais.
2. Que eu **atendo aos obrigatórios** (formação, SQL, Python, Linux) e as lacunas são de **ferramenta**,
   não de raciocínio nem de vontade.
3. Que as lacunas de ferramenta podem ser cobertas — **e não é discurso vazio: tem projeto no GitHub** (seção 9).
4. Que minha **experiência em ambiente regulado** (NASA, normas de qualidade) é transferível para Bacen.
5. Que o resultado de quem já foi barrado não muda o argumento: o candidato anterior caiu em pré-requisito de
   formação, o meu caso é o oposto — tenho a formação e falta a ferramenta.

**Mensagem que vou mandar para eles (rascunho em português natural):**

> Olá, [nome]. Meu nome é Francisco Renato Abreu. Sou engenheiro eletricista, trabalho com infraestrutura
> crítica na rede de radioastronomia IVS/NASA há 14 anos e hoje uso Python em produção para coletar,
> processar e monitorar dados de telemetria. É essa a minha base: automação, confiabilidade e documentação —
> que é exatamente o que a área de Risco de Crédito pede de um pipeline de dados.
>
> Sobre a stack: uso Python e SQL no dia a dia, trabalho com Linux e alta disponibilidade há mais de uma
> década, e estou me preparando a fundo em PySpark, Airflow e Kubernetes para entrar nessa camada. Já estou
> publicando um projeto próprio de pipeline de dados com a stack da vaga, justamente para mostrar que a
> transição é real e já está em andamento.
>
> Minha landing page está atualizada com os links do currículo, do LinkedIn e dos meus repositórios. Fico à
> disposição para conversar sobre a senioridade da vaga e alinhar expectativa.

> *(ajustar o tom e o tamanho conforme o canal — LinkedIn, e-mail ou WhatsApp exigem textos diferentes)*

**Ângulo de venda (versão curta, para LinkedIn):**
> Engenheiro de dados em transição, com 14 anos de operação de infraestrutura crítica (99,7% de
> disponibilidade) e Python em produção. Trago confiabilidade, governança e documentação — que é o que um
> pipeline de Risco de Crédito precisa para ser auditável.

**Pontos do currículo a destacar (ordem de impacto):**
- [ ] **Recém-produzido:** projeto de pipeline de dados com Spark + Airflow + Docker (seção 9) — mata 3 lacunas de uma vez
- [ ] Gestão de Ativos / 99,7% de disponibilidade / redução de MTTR em 35% → confiabilidade de dados
- [ ] Automação em Python com redução de 40% de processamento manual → ETL
- [ ] Dashboards de SLA e monitoramento remoto → observabilidade de pipeline
- [ ] Relatórios técnicos em inglês para rede NASA → documentação e comunicação com normas
- [ ] Gestão de estoque de 200+ itens críticos com otimização de lead time → logística
- [ ] Python: BAIXADOR-X, Clima Eusébio, FGO Data Update (GitHub)
- [ ] **Landing page** com links de currículo, LinkedIn e repositórios → vitrine do case

**Portfólio / anexos:**
- [ ] Currículo ATS (`arquivos-md/CURRICULO_ATS.md`) — versão customizada para esta vaga
- [ ] Currículo visual (`arquivos-pdf/`)
- [ ] GitHub: github.com/renatoapdl
- [ ] LinkedIn: linkedin.com/in/renatoabreuengenharia
- [ ] Projeto da stack da vaga (seção 9) — **o anexo que decide a candidatura**

---

## 8. PREPARAÇÃO PARA ENTREVISTA

### Perguntas prováveis (e o que a pergunta real está testando)
1. **Conte sobre sua experiência com pipelines de dados.** → profundidade real vs. profundidade de curso online
2. **Como você garante qualidade e confiabilidade de um pipeline em produção?** → validação, *profiling*,
   reconciliação, monitoramento de *freshness* e volume, alerta
3. **O que é governança de dados e o que a Resolução Bacen 4.966/21 muda na prática?** → resposta curta e honesta:
   "Comecei a estudar; sei que exige rastreabilidade e documentação das regras de risco" + o que minha
   experiência em ambiente auditado (NASA) me ensina
4. **Airflow e orquestração: como você modelaria uma DAG para cargas diárias de crédito?** → 5 camadas:
   *extract → landing (raw) → transform (staging) → quality gate → serve/consumo*; idempotência, *backfill*,
   alertas, retenção
5. **PySpark ou pandas: quando cada um?** → volume, partições, *shuffle*, memória contra cluster
6. **Kubernetes: por que usar no lugar de uma VM?** → orquestração, auto-scaling, self-healing, custo
7. **Conte sobre um problema técnico que você resolveu.** → caso NASA: 40% menos tempo manual, 35% menos MTTR
8. **Por que dados? Por que um banco?** → narrativa de transição, sem soar como "quero mudar de carreira"
9. **Quanto você espera ganhar?** → ver seção 10 (a coordenadora já perguntou ao amigo)

### Respostas / Argumentos prontos
- **SE perguntarem "você já trabalhou com dados?"** → "Trabalho com dados há anos: telemetria, coleta,
  processamento e dashboards. O que muda agora é o formato — de série temporal de telemetria para dados
  transacionais de crédito — mas a disciplina (coletar, validar, monitorar, documentar) é a mesma."
- **SE perguntarem sobre a falta de experiência bancária** → honesto e transferível: ambiente regulado NASA,
  normas de qualidade, documentação auditável, e que Risco de Crédito é domínio que se aprende em 90 dias
  (sem fingir que já sei)
- **SE perguntarem "você não é júnior demais para ser pleno?"** → inverter: "Minha senioridade é real em
  operação e confiabilidade; minha lacuna é de ferramenta específica. Já estou construindo o case da stack
  da vaga" — mostrar o repositório na hora, se possível
- **SE perguntarem a expectativa de salário** → ancorar no valor que o amigo repassar, e dizer que a senioridade
  importa mais que o valor fixo porque o valor é o do nível da vaga. **Nunca chutar número antes de saber a faixa.**

### Lacunas que preciso preparar antes da entrevista
- [ ] PySpark (partições, *shuffle*, *broadcast join*, `SparkSession`, DataFrame API)
- [ ] Airflow (DAG, operators, sensors, *backfill*, conexão com cloud, agenda)
- [ ] Hadoop / HDFS / Parquet / ORC (formato colunar, particionamento, compressão)
- [ ] Kubernetes (Deployment, Service, ConfigMap, volumes, Helm básico)
- [ ] MLOps (versionamento de modelo, *feature store*, monitoramento de *drift*, CI/CD de dados)
- [ ] Snowflake / AWS (Redshift, S3, Glue, Athena — o que o DOMO usa)
- [ ] Risco de crédito: PD, EAD, LGD, provisão IFRS 9, Basel III, RWA, *rating* interno
- [ ] Resolução Bacen 4.966/21: ler pelo menos o resumo e o capítulo de dados
- [ ] ETL contra ELT, CDC, *idempotência*, *upsert*, SCD Type 2 (o vocabulário da entrevista)

---

## 9. PLANO DE ESTUDO / CASE (orientações do amigo)

> **Objetivo:** cobrir as lacunas da seção 6 com artefato público, não só com curso.
> **Regra:** todo item de estudo precisa virar commit no GitHub antes da entrevista — a coordenadora disse que
> o RH olha projetos pessoais para medir domínio de ferramenta.
> **Laboratório:** **Databricks Community Edition** (cadastro gratuito) para treinar PySpark de verdade, sem
> instalar cluster local.

| # | Ferramenta | Objetivo mínimo (o que precisa saber fazer) | Onde demonstrar | Status |
|---|-----------|---------------------------------------------|-----------------|--------|
| 1 | **Python** | ETL real: ler, limpar, tratar nulos, definir valor padrão, criar campo derivado, salvar | Pipeline do item 9 | `[ ]` |
| 2 | **PySpark / Spark** | DataFrame API: ler e salvar (CSV/Parquet/Delta), criar campo derivado de um ou mais campos, limpeza, nulos | Job no Databricks CE + repositório | `[ ]` |
| 3 | **SQL** | Joins, CTE, window function, *upsert*, otimização de query | Queries comentadas + tasks do Airflow | `[ ]` |
| 4 | **Airflow** | DAG com as 5 camadas, *sensors*, *backfill*, agenda, alerta de falha | Repositório do pipeline | `[ ]` |
| 5 | **Kubernetes** | Comandos principais do `kubectl`, listar e descrever pods, ler log, *port-forward* | Manifests + doc com print de tela | `[ ]` |
| 6 | **Snowflake** | Básico (1-2 vídeos no YouTube): criar banco, schema, tabela e rodar SQL — lá é SQL | Script SQL + print do console | `[ ]` |
| 7 | **MLOps** | Versionamento de modelo, monitoramento de *drift*, CI/CD de dados | Serviço de *drift* sobre dados sintéticos | `[ ]` |
| 8 | **Risco de crédito** | PD, EAD, LGD, provisão IFRS 9, Basel, noções da Resolução 4.966/21 | Script de cálculo de provisão | `[ ]` |
| 9 | **Projeto case** | ETL de vendas em PySpark: CSV → Parquet bruto → limpeza → Parquet tratado, com README, diagrama e testes | `projetos/pipeline-etl-vendas/` | `[x]` rodando de verdade, 9 testes passando; falta publicar |

**Sequência sugerida:** 1 e 3 primeiro (são o que eu já uso), depois 2 (PySpark é o que mais aparece em vaga de
dados), depois 4 para amarrar o pipeline, 5 e 6 como camadas de infraestrutura, e 7 e 8 para fechar o discurso.

### 9.0 Projeto case — estado em 26/09/2026 (v2, simplificado)

**O projeto foi reescrito do zero.** A primeira versão (4 camadas, quality gate, DAG do Airflow,
Kubernetes, Snowflake e módulo de risco) está arquivada em
`_arquivo/pipeline-risco-credito-completo-2026-09-25.zip` e saiu do diretório ativo. O diretório ativo
também foi renomeado de `pipeline-risco-credito` para `pipeline-etl-vendas`, porque não é mais um projeto
de risco de crédito.

**Motivo da simplificação:** o amigo apontou que o case estava grande demais para eu dominar e
explicar, e a orientação dele era construir algo em ~2 dias. A versão complexa eu rodava, mas não
conseguia defender linha a linha — e isso apareceria em entrevista. O case novo faz exatamente o que
ele pediu: ler um CSV, gravar o bruto, limpar, criar um campo novo e gravar o resultado.

**O que existe agora** em `projetos/pipeline-etl-vendas/`:

| Arquivo | Linhas | O que faz |
|---------|--------|-----------|
| `etl/extract.py` | 35 | Lê o CSV com schema declarado, tudo como `string`, sem corrigir nada |
| `etl/transform.py` | 107 | 6 regras de limpeza + 1 campo derivado (`valor_total`) |
| `etl/load.py` | 18 | Grava Parquet em modo `overwrite` (idempotente) |
| `etl/run.py` | 75 | Executa e mostra o efeito de cada regra no log |
| `tests/test_transform.py` | 115 | 9 testes |
| `dados/vendas_bruto.csv` | 27 registros | Base sintética versionada, com sujeira proposital |

**Total: 235 linhas de código + 115 de teste.** Sem Airflow, Kubernetes, SQL, governança e sem módulo de
risco.

**As 6 regras, e o problema do CSV que cada uma resolve:**

| Regra | Problema real no arquivo |
|-------|--------------------------|
| R1 descartar incompletos | 1 linha sem `id_venda`, 1 sem `data_venda` |
| R2 padronizar datas | `2026-01-05` e `17/02/2026` na mesma coluna |
| R3 converter valores | `189,90` e `R$ 1.234,56` (formato brasileiro com e sem moeda) |
| R4 normalizar texto | `  Notebook  `, `CABO USB`, `CANCELADO` — espaço e caixa alta quebram agrupamento |
| R5 preencher nulos | `quantidade` e `situacao` vazias |
| R6 remover duplicadas | `VEN-0004` e `VEN-0011` chegam 2 vezes; fica a mais recente (`row_number` por data) |

**Validado de verdade, nesta máquina:**
- `pytest` → **9 testes passando**.
- Pipeline completo: **27 linhas extraídas → 25 após descartar incompletas → 23 após deduplicar**.
- Schema final tipado: `data_venda: date`, `quantidade: integer`, valores em `double`.
- **Idempotência confirmada:** execução repetida não duplicou linha.
- Conferências de negócio: 23 `id_venda` distintos, zero datas nulas, 1 venda sem `valor_unitario`
  (mantida nula de propósito, com aviso no log), situações 18 `aprovado` / 2 `cancelado` /
  2 `desconhecida` / 1 `pendente`; faturamento Web `28.285,02` em 15 vendas e loja `8.957,28` em 8.

**Bugs que só apareceram ao rodar** (todos corrigidos):
- **`189,90` virou `18990,0`.** O CSV tinha valores em dois formatos e a regra tratava ponto como milhar.
  O resultado estava 100× errado e **nada avisou** — a contagem continuava 23. Corrigi padronizando a
  entrada em formato brasileiro: número depende do sistema de origem, e adivinhar é pior do que exigir
  um formato só.
- **O teste passava e o dado real falhava.** A regra de situação vazia checava texto vazio (`""`), mas o
  Spark lê campo vazio de CSV como `null`. O teste montava o DataFrame com `""` e passava; o pipeline real
  deixava `situacao` nula. O teste virou parametrizado (`null` e `""`) e a regra passou a checar os dois.
- **`to_date` não aceita lista de formatos** no PySpark 3.5 (`Method to_date([Column, ArrayList]) does not
  exist`). Resolvido com `when` escolhendo o formato antes de converter.
- **`Python worker failed to connect back`** nos testes: o worker do Spark sobe o `python` que estiver no
  PATH, e aqui era um Python 3.14 sem o PySpark. Resolvido apontando `PYSPARK_PYTHON` e
  `PYSPARK_DRIVER_PYTHON` para o mesmo interpretador do driver.

**Falta para publicar:**
- [ ] `git init`, primeiro commit e repositório público no GitHub
- [ ] Badge de teste no README (os testes já rodam)
- [ ] Segundo degrau, só depois de publicado: quality gate que reprova + DAG no Airflow

**O que não está mais no projeto ativo** (era o que tornava tudo maior): DAG do Airflow, manifestos de
Kubernetes, CI, 6 consultas de SQL, módulo de risco (PD/EAD/LGD/ECL/RWA) e 4 documentos de arquitetura.
Tudo isso está no zip de backup, para quando eu subir o degrau.

### 9.1 Contexto do processo (transcrição do áudio, revisada)

> **Fonte:** áudio de WhatsApp do amigo, arquivo `candidaturas/audio-contexto.ogg` (4min28s).
> Transcrição automática com faster-whisper (modelo `small`, CPU), **revisada e corrigida**.
> Transcrição bruta em `candidaturas/audio-contexto.txt`.

#### Situação atual
- Havia **duas pessoas na lista** para a vaga. A **primeira (uma mulher) recusou a proposta**, aparentemente por
  motivo financeiro/salário.
- O **segundo candidato (homem) foi barrado no RH**: não tinha **formação superior completa** — apenas curso
  técnico. O banco exigiu a comprovação no fim do processo, depois das primeiras entrevistas, e a experiência
  dele até estava boa, mas não passou. **Foi o pré-requisito que matou a indicação.**
- **Consequência: a vaga vai ser reaberta.** É a janela atual.
- O amigo levou o assunto de novo no **one-on-one dele com a coordenadora do projeto** (coordenadora imediata
  do banco) e pediu **indicação de um Júnior** e também, em segunda opção, **um Pleno**.
- A coordenadora respondeu que **vai levantar quanto estão pagando** e que o banco **não gosta muito de abrir
  vaga assim** (fora de processo, por indicação), mas que **vai tentar extrair** essa possibilidade — inclusive
  para Pleno. Deixou claro que **não é nada certo**.
- Ela pediu explicitamente: **melhorar o LinkedIn antes**, porque **o RH filtra por LinkedIn e currículo mesmo
  com indicação** — e olha **projetos pessoais** para ver domínio de ferramenta.
- O amigo disse que me passa materiais de apoio nessa linha, e que **se eu não tiver nada, crie
  algo mais simples só para demonstrar conhecimento nas ferramentas**.
- A coordenadora perguntou a **expectativa de salário** e se eu **desenvolveria um Pleno** (talvez pelo salário
  ser melhor). O amigo respondeu que minha **capacidade de aprendizado é muito alta** e que me indicaria
  **até para Pleno**; chegou a dizer que, se colocarem um especialista ali, ele mesmo vai ter que ensinar
  muita coisa, e que qualquer pessoa que entre, em qualquer senioridade, tem curva de aprendizado nas
  primeiras semanas e meses.
- **Plano do amigo:** se a troca para Júnior ou Pleno sair, a **primeira alternativa é a minha contratação**.
- **Ressalva de ritmo:** via **Domo** a troca de senioridade é mais lenta do que se fosse direto com o banco,
  porque **atrás do Domo existe outro gestor** — se fosse pelo banco, ela teria contato direto com quem contrata.
- **Próximo passo dado pelo amigo:** me pediu para já **ajustar o LinkedIn com ajuda de IA** e **mandar para
  eles** (ele repassa ao RH).

#### Tarefas que saem do áudio (prioridade máxima)
- [ ] **LinkedIn no nível certo** — é o filtro do RH (áudio 01:27 a 01:43 e 04:08 a 04:19)
- [ ] **Projetos pessoais no GitHub** que provem domínio das ferramentas da vaga (áudio 01:43 a 02:11)
- [ ] Se eu não tiver nada pronto, **criar algo simples** só para demonstrar conhecimento nas ferramentas
- [ ] Definir **expectativa de salário** para Júnior e para Pleno (a coordenadora já perguntou)
- [ ] Ter resposta pronta para "**você desenvolveria um Pleno?**" (o amigo já respondeu por mim)

#### Áudios 2 a 9 — a parte que definiu o formato do case (26/09/2026)

O amigo mandou mais 8 áudios, transcritos com `tools/transcricao/transcrever.py` (faster-whisper `small`,
CPU, local). Transcrições em `candidaturas/audio-contexto2.txt` até `audio-contexto9.txt` (6,7 min).

Eles não mudam o contexto do processo — mudam **o escopo do case**. O que eles revelam:

**O amigo	validou a simplificação e definiu a escada.** Em ordem cronológica de execução:
1. Extrair de um arquivo (ou API) e salvar em formato performático — Parquet ou Delta.
2. Transformação simples: criar um campo derivado de outro campo, com regra de negócio simples.
3. Funções de tratamento de nulos, "pelo menos umas duas".
4. **Só depois**, na segunda parte, orquestrar com Airflow. "A princípio esse primeiro não precisa ser
   orquestrado."
5. E a **arquitetura medallion**: bronze (bruto extraído) → prata (transformação e criação de campos) →
   ouro (limpeza e entrega para o BI).

**Isso reorganiza o meu plano de estudo.** O `roadmap_vaga.md` punha Airflow como 3º item; para o case,
Airflow é degrau 2, e o medallion é a arquitetura que ele espera ver.

**Três correções concretas que os áudios impuseram:**

| Onde | O que eu tinha | O que ele disse | Efeito |
|------|----------------|-----------------|--------|
| Print da DAG | Tratado como bloqueado por Docker | "Pode ser mais a lógica mesmo, construir a DAG e as tasks, e gerar uma imagem de como ficaria" | Sai a dependência de Docker. O print é gerável sem executar |
| Evidência de execução | Print de cluster local (impossível sem Docker) | "Leva pro Databricks, exporta o código, tira um print, posta no GitHub" | Databricks Community Edition vira o caminho da evidência |
| Arquitetura | `bruto → tratado` em uma passada | Medallion de três camadas | Virou item de V2. A divisão fecha: prata leva tipagem e `valor_total`, ouro leva descarte, nulos e dedup |

**Uma oferta de dado, ainda pendente:** o amigo ofereceu mandar uma base pequena — CSV ou Parquet — com
dados de crédito, para substituir o CSV sintético. É o que a coordenadora pediu ("olha projetos pessoais"),
então é prioridade quando chegar.

**Onde eu me desviei, de propósito:** ele exemplificou tratamento de nulo como numérico → `0` e string →
`"IGNORADO"`, e disse explicitamente que se pode inventar. Usei `quantidade = 1`, `situacao = "desconhecida"`
e **deixo preço vazio como nulo**, porque `quantidade = 0` significaria venda de zero unidades e
`valor_unitario = 0` zeraria o faturamento sem ninguém perceber.

**Falso positivo que vale registrar:** a transcrição automática, que é boa mas não é infalível, produziu
fragmentos em coreano e em inglês no meio do texto em português, e um termo de risco de crédito saiu
traduzido para coreano (o original era "analista"). Revisei cada transcrição manualmente antes de usar. É a
razão de ler as transcrições em vez de copiá-las direto para o documento — e de nunca citar a transcrição
automática como se fosse o que o amigo disse.

**Itens que ele mesmo deixou para depois:** SQLite na entrega final ("talvez não esse primeiro projeto, mas
talvez com uma V2, V3") e API como fonte em vez de arquivo ("um arquivo também é super válido, só vai
mudar ali a fonte"). Ambos registrados como V2/V3.
- [ ] Currículo coerente com o LinkedIn — o RH olha os dois juntos

#### Como o áudio muda o plano (seção 6 → seção 9)
| Lacuna | O que o áudio pede | Item do plano |
|--------|--------------------|----------------|
| Projetos GitHub pequenos | "projetos pessoais" com domínio de ferramenta | Itens 1, 2 e 6 |
| Spark / Airflow / Kubernetes | "demonstrar domínio nas ferramentas" | Itens 1 e 3 |
| MLOps | "demonstrar domínio" | Item 4 |
| Domínio bancário | não citado no áudio | Item 5 |
| Formação superior | **foi o que reprovou o candidato 2** | já atendido (UNINTER) |

### 9.2 Roadmap de ferramentas indicado pelo amigo (mensagem de WhatsApp)

> **Mensagem literal dele (25/09/2026), na íntegra:** "Entendi... Tipo: **PYTHON**, **PYSPARK**, **SQL**,
> **AIRFLOW**, **KUBERNETES** (olhar os principais comandos, ver os pods no cluster, pegar um log e etc),
> **SNOWFLAKE** (básico só, ver um ou dois vídeos no YouTube, porque vai trabalhar com SQL lá dentro dele).
> Conhece **Databricks**? Faz o cadastro lá para treinar Spark, tem um cadastro para usar **free**.
> **PySpark** seria entender a sintaxe: ler um dado, salvar, criar um campo novo com base em um outro campo ou
> em mais de um campo, fazer uma limpeza de dados, tratar os nulos, definir um valor padrão para eles.
> Eu correria atrás de **projetos práticos para postar**. Algo que comprove experiência nas ferramentas é
> muito bom."

**Tradução em tarefas (o que isso significa na prática):**

| Dica dele | O que fazer de concreto | Critério de "pronto" |
|-----------|------------------------|---------------------|
| PySpark: ler, salvar, criar campo, limpar, tratar nulos | Script no Databricks CE ou cluster local | Consigo fazer sem copiar e colar tutorial |
| "Criar um campo novo com base em um ou mais campos" | Derived column: ex.: `idade = data_ref - data_nascimento`, `faixa de renda` | Está no repositório com comentário explicando a regra |
| "Limpeza de dados, nulos, valor padrão" | Normalizar strings, datas, deduplicar, preencher nulos com regra explícita | README explica cada regra de limpeza |
| Kubernetes: comandos principais, ver pods, pegar log | `kubectl get pods`, `describe`, `logs -f`, `port-forward`, `exec` | Documentado com print de tela real |
| Snowflake: básico, é SQL | Criar database, schema, tabela, view; *window function* e *upsert* | Script SQL rodável |
| Databricks free | Criar conta, subir um cluster, rodar o job de PySpark | Notebook público ou script no repositório |
| "Projetos práticos para postar" | Um projeto que use a stack, não curso solto | Repositório público com README e diagrama |

**Observação do amigo que importa:** ele prefere **prova prática postada** a certificado. O LinkedIn e o
GitHub são o vitrine — o conteúdo da mensagem para a recrutadora tem que apontar para lá.

### 9.3 Meu posicionamento e o que já respondi ao amigo

**O meu medo declarado:** assumir como Pleno e não atender às expectativas, no nível de **autonomia** e de
**domínio das ferramentas** exigidas. Isso é um risco real e precisa ser resolvido, não escondido. Três
saídas possíveis, em ordem de segurança:

1. **Aceitar Júnior com cláusula de revisão** (é o que o amigo está tentando). Risco baixo, mas salário menor
   e a candidata 1 já recusou por dinheiro.
2. **Aceitar Pleno com plano de rampa declarado** — "nos primeiros 90 dias, foco em X, Y, Z; a autonomia em
   Python e SQL já é minha hoje". Transforma a lacuna em plano e é defensável em entrevista.
3. **Aceitar Pleno e assumir o risco** — só faz sentido com o projeto case publicado antes de entrar.

**Minha conclusão:** o argumento não é o puro "não tenho experiência" e sim "tenho 14 anos de autonomia
operacional em infraestrutura crítica e estou chegando agora na camada de ferramenta". Isso é verdade e é
vendável.

**O que eu já tenho (portfólio atual):**
- **Downloader (BAIXADOR-X)** — Python, `yt-dlp`, CustomTkinter
- **Consumo de API de meteorologia (Clima Eusébio)** — Python, Tkinter, API REST com atualização automática
- **FGO Data Update** — Python/HTML, automação de dados de radioastronomia
- **Landing page pessoal** — front-end, já com links para currículo, LinkedIn e repositórios
- **Automação de telemetria no trabalho** — Python em produção (Mackenzie/NASA)

**Lacuna que eu mesmo identifiquei:** os projetos são pequenos e de app desktop, não de pipeline de dados.
É exatamente por isso que o projeto case (item 9) é necessário.

**LinkedIn — título atual:**
> Desenvolvedor Full-Stack | Engenheiro de Dados | Python | Especialista em Gestão de Ativos e Dados Críticos

Leitura para esta vaga: tem os termos certos, mas **"Full-Stack" ocupa a primeira posição e dilui a mensagem** —
para Engenharia de Dados, a primeira palavra precisa ser dados/engenharia de dados. Revisar ordem e tamanho
(título do LinkedIn corta em ~60 caracteres).

**Landing page:** já melhorada, com links para currículo, LinkedIn e repositórios. **Pedir para o amigo ver e
para a coordenadora olhar** — é o "case" de apresentação antes mesmo do projeto de pipeline ficar pronto.

### 9.4 Insights estratégicos do áudio
1. **O pré-requisito que elimina é "formação superior completa"** — eu já tenho, então isso me coloca à frente
   de quem concorre sem graduação. Vale confirmar se o RH exige **comprovação via diploma verificado**, porque
   foi exatamente na hora de comprovar que a indicação caiu.
2. **A falha da candidata 1 foi salário** — o valor de Júnior provavelmente é apertado. Se eu entrar como
   Júnior, a negociação salarial é o ponto sensível. **Pleno é o alvo mais fino**, e o próprio amigo prefere Pleno.
3. **O argumento de "capacidade de aprendizado" já está posicionado pelo amigo** — minha tarefa é sustentá-lo com
   prova concreta (projeto, commit, artigo), não só com discurso.
4. **Lentidão é o maior risco do processo**: a troca de senioridade depende de alguém do Domo/Banco decidir.
   Minha entrega (LinkedIn + projetos) é o que dá lastro ao pedido do amigo.
5. **Se a troca de nível não rolar**, o plano B é usar essa mesma preparação para vagas de dados em outros bancos
   e fintechs — o conteúdo é o mesmo.

### 9.5 O que eu preciso DOMINAR vs. o que eu só preciso saber MANTER

Dividir por arquivo do projeto, porque a pergunta "isso é infra ou é o meu trabalho?" decide onde eu gasto
tempo. Um Júnior e um Pleno **não** precisam do mesmo conhecimento: esperam que o Pleno resolva problema de
dados e apenas saiba manter a plataforma.

**No projeto atual, tudo é núcleo** — são 235 linhas e não há onde esconder o que não sei:

| Arquivo | Por que é núcleo |
|---------|------------------|
| `etl/transform.py` | São as 6 regras. Pergunta certa: "por que `row_number` e não `dropDuplicates`?" e "por que nem todo nulo foi preenchido?" |
| `etl/extract.py` | Schema declarado como tudo `string`. É a decisão que evita `189,90` virar `18990,0` |
| `etl/load.py` | `overwrite` é o que torna a execução idempotente — e por que rodar duas vezes não duplica |
| `etl/run.py` | O log por etapa é o que prova o efeito de cada regra; é a minha ferramenta de narrativa em entrevista |
| `tests/test_transform.py` | Preciso saber o que cada um dos 9 testes prova, não só que passa |
| `dados/vendas_bruto.csv` | A sujeira do arquivo é a justificativa de cada regra. Se eu não sei por que a linha existe, não sei a regra |

**Ainda assim é infra (mas não está no projeto ativo, fica no zip de backup):**

| Onde | Profundidade suficiente |
|------|-------------------------|
| `Dockerfile`, `docker-compose.yml` | Instalar Java/PySpark, volume, dependência entre serviço e health check |
| Manifestos de Kubernetes | `get/describe/logs/exec/port-forward`, ConfigMap, Secret, PVC, Job, resources |
| `.github/workflows/ci.yml` | Alterar passos, cache, subir badge. Não preciso reescrever Actions do zero |
| `SparkSession.builder` | Entender driver/executor, `spark.master`, partições e *shuffle* — sem querer reimplementar Spark |
| DAG do Airflow | Dependência, retry, *backfill*, e por que o quality gate é um artefato entre processos |
| Databricks Community Edition | Subir arquivo, rodar notebook, exportar código. Ferramenta, não domínio |

**Regra prática:** se eu não consigo explicar a decisão e o trade-off, é núcleo. Se eu consigo rodar, ler o log e
corrigir, é infra.

**Por que isso importa agora:** com o case simplificado, a lista de núcleo é curta e eu consigo memorizar. O
risco deixou de ser "não sei o código" e passou a ser "não explico bem" — que se resolve reescrevendo
(ver 9.7).

**O que o medallion acrescenta a esta lista** (quando subir para V2, ver 9.1): a distinção entre
**transformar** (tipar, criar campo, enriquecer) e **limpar** (descartar, preencher nulo, deduplicar) vira
uma camada física, e não só uma ordem de funções. É a resposta que a vaga quer para "como modelaria uma DAG
para cargas diárias de crédito", e ela só fica crível depois de eu defender a ordem das regras.

### 9.6 Plano de estudo com contexto (o que é prioritário e por quê)

Ordem deliberada: cada item só faz sentido depois do anterior, e todos reaproveitam o mesmo projeto.

> **Sequência que o próprio amigo ditou nos áudios 2 a 9**, e que organizei o plano:
> extrair → salvar em Parquet/Delta → criar campo derivado → tratar nulos → **só então** orquestrar com
> Airflow → e a arquitetura medallion (bronze/prata/ouro) como destino. O plano abaixo respeita essa
> ordem, porque ela é a ordem em que cada conceito sustenta o próximo.

**1º — PySpark DataFrame e Window (prioridade máxima, ~2 semanas)**
É o centro de tudo e o que mais derruba candidato em entrevista de dados. Preciso: `select/withColumn/filter/join`,
`groupBy/agg`, `Window.partitionBy/orderBy` com `row_number` e `lag`, `coalesce`/`when`/`otherwise`, escrita em
Parquet com `partitionBy`, e noção de driver vs. executor e *shuffle*.
- Documentação: [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- Prática: reescrever as 6 regras de `etl/transform.py` **do zero**, sem olhar, até passar. Depois explicar por
  que cada uma existe.
- Como vou ser avaliado: "como você deduplica mantendo a linha mais recente?" → `row_number` com
  `orderBy(data_venda desc)` e filtro `= 1`. Resposta de 1 minuto.

**2º — SQL analítico (~1 semana, melhor custo-benefício)**
`CTE`, `window function` (`row_number`, `lag`, `sum over`), `PERCENT_RANK`, `MERGE` (upsert) e filtro de
partição. Não há SQL no projeto atual — é a próxima coisa que eu escrevo, e reaproveito o mesmo CSV.
- Prática: escrever as consultas do zero e explicar a pergunta de negócio que cada uma responde.

**3º — Airflow (~1 tarde, sem clichê)**
Preciso de: DAG como código, `>>`, `default_args` (retry/backoff), `catchup` e *backfill* com data lógica
(`{{ ds }}`), XCom, *sensors*, e por que o quality gate é um arquivo em disco e não um retorno de função.
- Documentação: [Airflow — tutoriais e conceitos](https://airflow.apache.org/docs/apache-airflow/stable/)
- Atenção: a versão atual é a 3.x, e a 2.9.3 é a que estava fixada no case antigo (no zip). Preciso decidir se
  atualizo ou se sei explicar a escolha. É exatamente o tipo de pergunta que entrevistador de dados faz.
- Como vou ser avaliado: "por que cada camada é uma tarefa e não uma?" → porque cada uma reprocessa sozinha,
  em outra data e por outra máquina, e o gate precisa ser um artefato entre processos.

**4º — Kubernetes só o dia a dia (~1 tarde)**
O suficiente é: ver pod, descrever, log, entrar, port-forward, e saber o que é ConfigMap, Secret, PVC, Job,
Deployment, resource limit e health check. **Não** preciso saber admission controller, CNI ou manifesto de
ingresso — isso é de outro cargo.
- Prática: [Killercoda — Kubernetes](https://killercoda.com/kubernetes), um cenário de troubleshooting, e
  colar a saída real em um doc.

**5º — Databricks e Snowflake noções (~2 dias cada)**
Não é para virar especialista: é para não passar vergonha. Databricks Community Edition é grátis e roda o
pipeline inteiro; Snowflake é SQL sobre storage em nuvem — criar database/schema/table/view, e Medallion é o
mesmo bronze/silver/gold que o case antigo usava.
- Material gratuito oficial: [Mastering Data Engineering with Spark e Databricks](https://pages.databricks.com/mastering-DE-with-databricks.html)

**6º — Governança, IFRS 9 e Basel (lacuna crítica da seção 6)**
Vocabulário e raciocínio, não fórmula de exame: ECL = PD × LGD × EAD, provisões IFRS 9, Basel/Res. 4.966/21
sobre rastreabilidade, *overrides* de analista e revisão de modelo. O módulo `provisoes.py` e o doc de governança
estão no zip de backup, fora do projeto ativo; preciso saber **por que** cada control existe em um ambiente
regulado.

### 9.7 O que deste repositório foi gerado por IA — e o que eu preciso reescrever à mão

O código foi escrito com assistência de IA, e isso não é problema **se** eu souber explicar cada linha. O risco
real é a entrevista fazer uma pergunta de detalhe e eu descobrir na hora que não entendo o próprio projeto.
Reescrever à mão é o que converte "projeto publicado" em "projeto dominado".

**Preciso reescrever do zero (uns dois dias, é o melhor investimento do plano):**
1. `etl/transform.py` inteiro — as 6 regras, no editor, do zero, cada uma com o motivo do negócio escrito
   junto. É o arquivo que a entrevista vai abrir.
2. `etl/extract.py` — o schema declarado na mão, para fixar a decisão de ler tudo como `string`.
3. **Três testes que eu desenhei**, não que eu adaptei: um que hoje falha por um motivo que eu ainda não
   tinha pensado, um de propriedade e um de borda (data em formato inesperado, valor `0`, `quantidade`
   negativa).
4. **Uma consulta SQL nova** que responda a uma pergunta de negócio que ainda não respondi com SQL: qual
   canal concentra mais faturamento por venda?
5. Um commit meu de correção de bug — hoje os 4 bugs foram encontrados por mim **rodando**, mas preciso
   escrever pelo menos uma correção do zero e explicar a causa raiz.

**Preciso ler com atenção (não reescrever):** `etl/load.py` e o `run.py` — para explicar idempotência, e por
que o log mostra o efeito de cada regra em vez de só dizer "terminou".

**Não preciso reescrever agora:** Dockerfiles, manifestos do k8s e YAML do CI. Não estão no projeto ativo,
estão no zip, e quando eu os trazer de volta é infra — e é honesto dizer isso.

### 9.8 Além de publicar: o que falta para virar prova de verdade

- [ ] **Reescrever à mão** o núcleo (9.7) — sem isso o repositório é só um trabalho de terceiros, e isso
      aparece na entrevista.
- [ ] **Histórico de commit honesto**: um `initial commit` gigante com tudo empurra para a mesma coisa que
      quero evitar. Melhor: 3 ou 4 commits lógicos ("extrai e grava o bruto", "as 6 regras de limpeza",
      "dedup com row_number", "testes e README").
- [ ] **Um post curto no LinkedIn** sobre os 4 bugs que só apareceram ao rodar. É o material mais forte que
      eu tenho: é raro, é verificável e mostra senioridade sem eu precisar dizer que tenho. O do `18990,0`
      serve de abertura: erro 100× que nenhum alerta pegou, porque contagem de linha não detecta valor errado.
- [ ] **Resposta pronta de "o que você faria diferente em produção?"** — Delta Lake em vez de Parquet puro,
      CDC em vez de carga por lote, teste de contrato de esquema na entrada, regra de qualidade com
      percentual de tolerância (e não só zero/um), alerta de *drift* do scorecard, particionamento por data
      e custo por execução.
- [ ] **Segundo degrau do projeto**, depois de publicado: quality gate que reprova a publicação e DAG no
      Airflow. Só faz sentido com o primeiro dominado.
- [ ] **Subir no Databricks Community Edition** e colar o print no README. É o que o amigo pediu
      explicitamente ("leva pro Databricks, exporta o código, tira um print") e é a evidência que hoje
      eu não tenho. Exige cadastro, feito por mim no navegador.
- [ ] **Print da DAG**, gerado da lógica da DAG e das tasks, sem precisar executar o Airflow (áudio 3).
- [ ] **Base real**: quando o amigo mandar o CSV/Parquet dele, substituir o sintético e rodar de novo.
- [ ] **Decidir a versão do Airflow** (2.9.3 fixado no projeto antigo × 3.x atual) e saber justificar.
- [ ] **Atualizar o LinkedIn**: colocar "Engenharia de Dados" antes de "Full-Stack" (ver 9.3).

<!-- TRANSCRICOES -->

---

## 10. HISTÓRICO / STATUS

| Data | Evento |
|------|--------|
| 25/09/2026 | Amigo tenta convencer a coordenadora a abrir vaga **Júnior ou Pleno** para o perfil |
| 25/09/2026 | Candidata 1 (mulher) **recusou a proposta** (motivo financeiro) |
| 25/09/2026 | Candidato 2 (homem) **reprovado no RH**: sem formação superior completa |
| 25/09/2026 | Confirmação: **a vaga será reaberta** |
| 25/09/2026 | Coordenadora pede **LinkedIn ajustado + projetos pessoais** antes de avançar |
| 25/09/2026 | Coordenadora pergunta **expectativa de salário** e se eu desenrolaria um **Pleno** |
| 25/09/2026 | Amigo envia **roadmap de ferramentas** (seção 9.2) e reforça: projeto prático posted > certificado |
| 25/09/2026 | Landing page melhorada com links de currículo, LinkedIn e repositórios |
| 25/09/2026 | LinkedIn atualizado com novo título (ver ressalva em 9.3 sobre "Full-Stack" na frente) |
| 25/09/2026 | Meu medo declarado para o amigo: assumir Pleno sem entregar autonomia e domínio das ferramentas |
| 26/09/2026 | **Feedback do amigo: o case estava complexo demais** (4 camadas, quality gate, Airflow, k8s, Snowflake). Ele pediu algo que coubesse em ~2 dias e que eu conseguisse dominar |
| 26/09/2026 | **Case reescrito do zero:** ETL de vendas PySpark, 235 linhas, CSV → Parquet bruto → limpeza → Parquet tratado, com 6 regras e 9 testes. Versão antiga arquivada em `_arquivo/pipeline-risco-credito-completo-2026-09-25.zip` e removida do diretório ativo |
| 26/09/2026 | **4 bugs achados rodando** (o mais instructive: `189,90` → `18990,0`, 100× errado sem nenhum alerta). Documentados no README e na seção 9.0 |
| 26/09/2026 | `roadmap_vaga.md` reescrito na v2 para refletir o case simples, e enviado ao amigo |
| 26/09/2026 | **Mais 8 áudios do amigo** (6,7 min), transcritos com `tools/transcricao/transcrever.py`. Eles **validam a simplificação** e definem a escada: extrair → Parquet → campo derivado → nulos → (depois) Airflow, com arquitetura medallion como destino (seção 9.1) |
| 26/09/2026 | **Correção de plano:** o print da DAG não depende de Docker (dá para gerar da lógica), e a evidência de execução passa a vir do Databricks, não de cluster local |
| 26/09/2026 | **Oferta pendente do amigo:** mandar uma base pequena (CSV ou Parquet) com dado de crédito para substituir o CSV sintético |
| 26/09/2026 | Decidido: **medallion bronze/prata/ouro fica para a V2**, e a divergência no tratamento de nulo (`1`/`"desconhecida"` em vez de `0`/`"IGNORADO"`) fica registrada nos documentos internos, não no README |
| <!-- dd/mm/aaaa --> | <!-- Coordenadora retorna faixa salarial / decisão de nível --> |
| <!-- dd/mm/aaaa --> | <!-- Indicação repassada ao RH --> |
| <!-- dd/mm/aaaa --> | <!-- Entrevista --> |

**Próxima ação:** enviar LinkedIn ajustado + 1 projeto de dados publicado, e alinhar a expectativa salarial
com o valor que o amigo repassar
**Prazo:** <!-- definir com a coordenadora -->

**Pontos em aberto (perguntar ao amigo):**
- [ ] Qual o valor de **Júnior** e de **Pleno** que ela sabe?
- [ ] Ela já falou com o **gestor do Domo** ou ainda é só intenção?
- [ ] Ela aceita **PJ** ou é **CLT**?
- [ ] O RH exige **diploma verificado**? (foi o que derrubou o candidato 2)
- [ ] Quando reabrem a vaga? Existe **prazo**?
- [ ] Que materiais ele ia me passar sobre as ferramentas?

---

## 11. RESULTADO / APRENDIZADO

<!-- Preencher ao final: o que funcionou, o que não funcionou, ajustes para a próxima candidatura. -->

---

*Documento criado e mantido em Setembro de 2026 — pasta `candidaturas/`*
