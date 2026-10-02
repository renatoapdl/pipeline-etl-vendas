# Roadmap e Preparação — Vaga Engenharia de Dados
**Banco Mercantil / Domo — indicado por <Emerson>**
Atualizado em 29/09/2026 
---
## TL;DR
1. Reescrevi o projeto case do zero, **bem mais simples**: um ETL de vendas em PySpark, **235 linhas de código**, que faz exatamente o que você pediu — ler um CSV, gravar o bruto em Parquet, limpar e transformar, e gravar o resultado em Parquet.
2. **Roda de verdade:** 27 linhas entram, 23 saem, em ~15 segundos, com 9 testes automatizados passando.
3. Os dados são **sintéticos** e estão no repositório, com sujeira proposital para cada regra ter um motivo.
4. Achei e corrigi **4 bugs rodando** — inclusive um que fazia `189,90` virar `18990,0` sem nenhum aviso.
---
## 1. O que foi pedido e o que já existe
O roadmap que você mandou era: Python, PySpark, SQL, Airflow, Kubernetes, Snowflake (básico) e Databricks. Situação de cada item hoje:

| Item           |  Situação    | Onde está                             | Falta 
-----------------------------------------------------------------------------------------------
| **Python**     |  Coberto     | Todo o pipeline                     | Nada
| **PySpark**    |  Coberto     | CSV  Parquet bruto  Parquet tratado | Fundamentar *shuffle*
| **SQL**        | Iniciado     | Resolvendo desafio no Databricks    | concluir e publicar 
| **Airflow**    | Não iniciado | — | Vem depois do SQL, como evolução do projeto |
| **Kubernetes** | Não iniciado | — | Não é prioridade agora |
| **Snowflake**  | Não iniciado | — | 2 dias, mais adiante |
| **Databricks** | Iniciado     | Resolvendo desafio                  | Concluir desafio e testar o ETL lá 
| **MLOps**      | Não iniciado | — | Vem com o CI, na segunda etapa |

**Sobre a orientação "projetos práticos valem mais que certificado":** é a linha que segui.

### O que mudou depois de ouvir os seus 8 áudios
1. **"O primeiro não precisa ser orquestrado."** Está assim: a V1 é o ETL puro, sem Airflow. Airflow é a segunda parte.
2. **O print da DAG não precisa de Docker.** Você disse que o Airflow pode ser só a lógica — montar a DAG e as tasks — e gerar a imagem de como o pipeline ficaria. Eu tinha tratado o print como bloqueado por Docker, e não está. Isso tira um item da lista de dependências.
3. **A evidência nasce no Databricks.** Subir o CSV no Databricks Community Edition, exportar o código e tirar o print é o caminho que você indicou, e não depende de nada local. É o que falta para o README ter uma imagem de verdade.
---
## 2. O projeto case
**Repositório:** `projetos/pipeline-etl-vendas/`
### O que ele faz
```
dados/vendas_bruto.csv  →  data/bruto/vendas  →  limpeza e transformação  →  data/tratado/vendas
        (CSV sujo)          (Parquet como chegou)                             (Parquet limpo)
```
Quatro arquivos, uma responsabilidade cada:
| Arquivo                   | Linhas | O que faz 
-------------------------------------------------------------------------------------
| `etl/extract.py`          |   35   | Lê o CSV com schema declarado, tudo como texto 
| `etl/transform.py`        |   107  | 6 regras de limpeza + 1 campo derivado 
| `etl/load.py`             |   18   | Grava Parquet 
| `etl/run.py`              |   75   | Executa e mostra o efeito de cada regra no log 
| `tests/test_transform.py` |   115  | 9 testes 

### A sujeira do CSV e a regra que existe por causa dela

| O que tem no CSV         | Regra |
-----------------------------------------------------------------------------------------------
| `189,90` e `R$ 1.234,56` | tira o `R$`, remove o ponto de milhar, troca a vírgula por ponto e vira número |
| `2026-01-05` e `17/02/2026` | as duas viram data |
| `  Notebook  `, `CABO USB`, `CANCELADO` | espaço nas pontas e caixa alta quebram agrupamento |
| `quantidade` e `situacao` vazias | quantidade vira 1; situação vira `desconhecida` |
| `VEN-0004` e `VEN-0011` chegam 2 vezes | fica a linha mais recente (`row_number` por data) |
| 1 linha sem ID e 1 sem data | são descartadas e aparecem na contagem |

Resultado: **27 linhas entram, 23 saem**, nenhum ID repetido, nenhuma data nula.

### Os 4 bugs que só apareceram ao rodar
1. **`189,90` virou `18990,0`.** Meu CSV tinha valores em dois formatos e eu tratava ponto como milhar. Omresultado estava 100× errado, a contagem continuava 23. Corrigi padronizando a entrada em formato brasileiro: Número depende do sistema de origem, e adivinhar é pior que exigir um formato só.
2. **O teste passava e o dado real falhava.** A regra checava texto vazio, mas o CSV entrega nulo. O teste montava o dado do jeito errado e passava. O teste virou parametrizado para os dois casos.
3. **`to_date` não aceita lista de formatos** no PySpark 3.5. Resolvido escolhendo o formato antes de converter.
4. **`Python worker failed to connect back`** nos 7 testes: o worker do Spark sobe o `python` do PATH, que era um Python 3.14 sem o PySpark. Resolvido apontando para o mesmo interpretador do driver.

### O que ainda falta para publicar
- [x] `git init` e repositório público no GitHub
- [ ] Badge de teste no README (os testes já rodam)
- [ ] Subir o CSV no Databricks Community Edition, exportar o código e colar o print no README
- [ ] Trocar o CSV sintético pela base real.

### O que fica para a V2 
| Item | Origem da ideia |
|------|-----------------|
| **Arquitetura medallion: bronze → prata → ouro** | Você descreveu em dois áudios: bronze é o bruto extraído, prata é a transformação com a criação dos campos, ouro é a limpeza e a entrega final para o BI. Hoje eu faço `bruto → tratado` em uma passada só. A divisão fecha: prata leva a tipagem e o `valor_total`, ouro leva descarte, nulos e dedup. |
| **Entrega final em SQLite** | Você mesmo deixou de fora da V1: "talvez não esse primeiro projeto... talvez com uma V2, V3". Faz sentido, porque Parquet num path local não é exatamente "entregue para o BI" — um `SELECT` é. |
| **Fonte por API em vez de arquivo** | Você sugeriu, com CENIPA de exemplo, e falou que talvez nem tenha API. Você também disse que "um arquivo também é super válido, só vai mudar ali a fonte". Concordo: API fica para quando o ETL estiver dominado. |
| **One-hot encoding** | `dbt_masculino` / `dbt_feminino` com 1 e 0, que você citou como uso em modelo de ML. É mais um exemplo de campo derivado, e o `valor_total` já cumpre esse papel na V1. |
Um detalhe técnico que a divisão em medallion revelaria, e que vale eu saber antes: hoje o descarte de linha incompleta roda **antes** de converter a data. Então uma data presente mas inválida (`31/31/2026`) passaria
pelo filtro e viraria nula na conversão, sobrevivendo na saída. Se o descarte passar a rodar depois da conversão, ela é capturada junto. No CSV de hoje não existe data inválida, então o teste passa — mas é um furo que só apareceria com dado novo.
---
## 3. O que este projeto prova, e o que não prova
**Prova:** sei ler CSV com schema declarado, sei limpar dado real (nulo, duplicata, formato, texto), sei gravar Parquet tipado e comprimido, sei testar, e sei explicar por que fiz cada escolha.

**Ainda não prova:** orquestração, qualidade com bloqueio, particionamento, Delta Lake e cloud.

**Por que começar assim:** é o que eu consigo defender em 2 minutos de conversa. A versão complexa eu consigo rodar, mas não consigo explicar linha a linha — e na entrevista isso apareceria.
---
## 4. Plano de estudo priorizado

| # | Tema | Tempo | Por que essa ordem |
|---|------|-------|--------------------|
| 1 | **PySpark DataFrame e Window** | ~2 semanas | É o centro de tudo e o que mais reprova candidato em entrevista de dados |
| 2 | **SQL analítico** | ~1 semana | Melhor custo-benefício; é onde a vaga pede mais |
| 3 | **Airflow** | ~1 tarde | Preciso de DAG, *backfill* e por que o quality gate é um arquivo entre processos |
| 4 | **Kubernetes dia a dia** | ~1 tarde | Ver, descrever, logar, entrar no pod, *port-forward* |
| 5 | **Databricks e Snowflake** | ~2 dias cada | Para não passar vergonha; Medallion é o mesmo bronze/silver/gold |
| 6 | **Governança, IFRS 9 e Basel** | ~1 semana | Vocabulário do domínio regulado, que é a lacuna real |

**Recursos** (todos gratuitos e oficiais quando possível):
- Spark SQL e DataFrames: `spark.apache.org/docs/latest/sql-programming-guide.html`
- Airflow: `airflow.apache.org/docs/apache-airflow/stable/`
- Kubernetes na prática: `killercoda.com/kubernetes`
- Spark e Databricks: `pages.databricks.com/mastering-DE-with-Databricks.html`

**Como vou comprovar o progresso:** cada tema fechado vira um commit no repositório, e escrevo no README o que mudei.
---
## 5. Preparação para a entrevista

### Perguntas prováveis (e o que cada uma realmente testa)
1. **Conte sobre sua experiência com pipelines.** → profundidade real versus profundidade de curso
2. **Como você garante qualidade de um pipeline em produção?** → validação, *profiling*, reconciliação, monitoramento de volume e frescor do dado, alerta
3. **O que a Resolução 4.966/21 muda na prática?** → resposta curta e honesta: comecei a estudar; sei que exige rastreabilidade e documentação das regras de risco
4. **Como modelaria uma DAG para cargas diárias de crédito?** → as camadas, idempotência, *backfill*, alertas
5. **PySpark ou pandas, quando cada um?** → volume, partições, *shuffle*, memória
6. **Kubernetes: por que não uma VM?** → orquestração, auto-scaling, self-healing, custo
7. **Conte um problema técnico que resolveu.** → o caso do `18990,0`: bug que só apareceu rodando, e a decisão de não "consertar" adivinhando o formato do número
8. **Por que dados? Por que um banco?** → narrativa de transição, sem soar como mudança de carreira
9. **Quanto espera ganhar?** → ancorar na faixa que você repassar

### Respostas prontas
- **Se perguntarem se já trabalhei com dados:** trabalho com dados há anos — telemetria, coleta,
  processamento e dashboards. Muda o formato (série temporal para transacional de crédito), não a
  disciplina: coletar, validar, monitorar, documentar.
- **Se perguntarem da falta de experiência bancária:** tenho 14 anos em ambiente regulado e auditado (NASA), com norma de qualidade e documentação auditável. Risco de crédito é domínio que se aprende em 90 dias, e não vou fingir que já sei.
- **Se perguntarem se não sou júnior demais para Pleno:** minha senioridade é real em operação e
  confiabilidade; minha lacuna é de ferramenta específica, e o projeto mostra que eu aprendo rápido — está no README a lista dos 4 bugs que achei rodando. Se possível, mostro o repositório na hora.
- **Se perguntarem a expectativa de salário:** ancoro no valor que você repassar. Senioridade pesa mais que valor fixo, porque o valor é o do nível da vaga. Nunca chuteio número antes de saber a faixa.

### Lacunas que estou fechando antes da entrevista
- [ ] PySpark: partições, *shuffle*, *broadcast join*, API de DataFrame
- [ ] SQL: CTE, *window function*, *upsert*, *grouping sets*
- [ ] Airflow: DAG, operadores, sensores, *backfill*
- [ ] Hadoop/HDFS/Parquet/ORC: formato colunar, particionamento, compressão
- [ ] Kubernetes: Deployment, Service, ConfigMap, volumes
- [ ] Snowflake e AWS (Redshift, S3, Glue, Athena)
- [ ] Risco: PD, EAD, LGD, provisão IFRS 9, Basel III, RWA
- [ ] Resolução 4.966/21: resumo e capítulo de dados
- [ ] ETL contra ELT, CDC, idempotência, *upsert*, SCD Tipo 2
---
## 6. Plano de rampa, se entrar como Pleno

- **Dias 1–30:** ambiente, meus pipelines rodando em todos os ambientes, sombra dos processos de carga diária e revisão de pipelines existentes. A autonomia em Python e SQL já é minha hoje.
- **Dias 31–60:** primeira entrega de regra de qualidade ou feed novo do meu lado, com documentação e monitoramento.
- **Dias 61–90:** assumo um pipeline inteiro, incluindo a parte de infraestrutura.

Se a abertura for como **Júnior**, o plano é o mesmo e eu chego mais rápido. Prefiro **Pleno**
---
## 7. Próximos passos

| O quê                                           | Prazo               |Depende|Status|
--------------------------------------------------------------------------
| Publicar o repositório no GitHub                | Esta semana         | Nada  | [x]  | 
| Reescrever as 6 regras e os 9 testes            | Antes da entrevista | Nada  | [ ]  |
| Começar SQL analítico e subir 1 projeto próprio | Próxima semana      | Nada  | [ ]  |
| Segundo degrau do projeto       (conferir v2)   | Depois da publicação| Nada  | [ ]  |
| Modelar Linkedin para Engenharia de Dados       | Enviado ajuste pende| Nada  | [x]  |
| Ajustar o currículo com o LinkedIn              | Antes do RH         | Nada  | [x]  |