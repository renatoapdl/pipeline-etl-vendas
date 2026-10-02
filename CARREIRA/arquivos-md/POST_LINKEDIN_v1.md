# Post LinkedIn — Rascunhos v2 (Engenharia de Dados)

## Opção 1: Post de Transição (Recomendado para começar)

---

**De engenheiro de confiabilidade da NASA a engenheiro de dados**

Há 14 anos, opero e mantenho um dos maiores rádio telescópios do Brasil, o Rádio Observatório Espacial do Nordeste, vinculado à rede global IVS-NASA.

Nesse tempo, aprendi que confiabilidade não é opcional. Cada sensor, cada motor, cada pipeline que mantém um sistema de missão crítica funcionando exige rigor técnico e mentalidade de dados.

Recentemente, essa atuação evoluiu.

Comecei a usar Python para automatizar a coleta e o processamento de dados de telemetria no observatório:
- Scripts que reduziram em 40% o tempo manual de processamento
- Automação da atualização de dados VLBI
- Dashboards de performance (MTTR, SLA) em Grafana

E percebi que a engenharia de dados não é tão diferente da engenharia de confiabilidade:

MTTR é o tempo até um pipeline voltar a funcionar. Manutenção preditiva é data quality antes de o problema virar incidente. Telemetria são os pipelines de dados. Confiabilidade é qualidade de dados.

Agora, estou em transição ativa para **Engenharia de Dados**, com foco em:

- Python
- PySpark (ETL)
- SQL

Meu primeiro case já está de pé: um pipeline ETL de vendas em PySpark que valida, limpa e carrega dados em Parquet (27 → 25 → 23 registros válidos, com 9 testes automatizados).

Se você também está em transição de carreira, saiba: sua experiência anterior não é peso, é diferencial.

---

O que vocês acham? Alguém mais aqui fazendo essa transição?

#TransiçãoDeCarreira #EngenhariaDeDados #Python #PySpark #DataEngineering #CareerChange

---

## Opção 2: Post Técnico

---

**O que gestão de ativos tem a ver com qualidade de dados?**

No Rádio Observatório Espacial do Nordeste (NASA/Mackenzie), gerencio a confiabilidade de sistemas de radioastronomia há 14 anos.

Os conceitos são os mesmos:

- MTTR (Mean Time To Repair) é o tempo médio para resolver um incidente. Em dados, é quanto tempo leva para um pipeline falhar e ser corrigido.
- SLA (Service Level Agreement) é o acordo de nível de serviço. Em dados, é garantir que os dados chegam no prazo esperado, e corretos.
- Disponibilidade (99.7%) é o tempo que o sistema deve ficar no ar. Em dados, é o uptime do pipeline e a qualidade do dado entregue.
- Data Quality é o que eu chamava de confiabilidade na manutenção. Em dados, validação, limpeza e observabilidade.

A engenharia de dados é, no fim, gestão de ativos para dados.

Quem já trabalhou com sistemas de missão crítica tem uma vantagem: mentalidade de confiabilidade.

---

#EngenhariaDeDados #DataEngineering #DataQuality #Python #PySpark

---

## Opção 3: Post Pessoal (Para gerar engajamento)

---

**3 lições de confiabilidade que aplico nos meus pipelines**

Trabalho com sistemas de missão crítica há 14 anos. Cada lição se aplica a engenharia de dados:

**1. Monitore antes de precisar**
Não espere o dado errado chegar ao relatório. Monitore logs, métricas e alertas. Em dados: observabilidade de pipeline e quality checks.

**2. Valide na entrada, não na saída**
Um dado inválido que entra silenciosamente corrompe todo o downstream. Em dados: validação na ingestão (no meu pipeline ETL, 27 → 25 → 23 registros válidos).

**3. Documente como se sua vida dependesse disso**
Porque alguém vai precisar manter seu pipeline um dia. Em dados: README de arquitetura, testes automatizados e schema documentado.

Essas lições vêm da engenharia elétrica, mas se aplicam a qualquer pipeline.

---

Qual lição de outra área você aplica nos seus dados?

#BoasPráticas #EngenhariaDeDados #Python #Confiabilidade

---

## Opção 4: Post de Case (Quando o GitHub estiver no ar)

---

**Case: um pipeline ETL de vendas em PySpark (27 → 25 → 23)**

Construí um pipeline ETL que extrai um CSV de vendas, valida e limpa os dados, e carrega em camadas bruto/tratado em Parquet.

O que ele faz:
- Extração de vendas (CSV)
- Validação e limpeza (preços, quantidades, datas, região)
- Carga em Parquet (camada bruta + tratada)
- Sumarizações: faturamento e ticket médio por região/período
- 9 testes automatizados para garantir que o pipeline não quebra silenciosamente

O número 27 → 25 → 23 são os registros que sobraram depois da validação. Foi exatamente aí que os conceitos de confiabilidade da minha área de origem entraram: **dado inválido não entra**.

[Link do repositório]

---

#EngenhariaDeDados #PySpark #ETL #Python #Portfolio

---

## Opção 5: Post de Case Databricks (quando o repo estiver no ar)

---

**Case Databricks: do bronze ao ouro em uma única consulta SQL**

Montei um case de tratamento de dados no Databricks SQL com base em um desafio real de processo seletivo.

O problema: 40 registros cheios de sujeira de qualidade de dado.

- idades negativas
- emails sem @
- datas impossíveis (mês 15, dia 40)
- CPF com letras
- salários e dívidas negativos
- estado "InvalidState" e país grafado errado

O desafio pedia: **13 regras de negócio em uma única consulta SQL**.

O que eu entreguei:
- Um SELECT com todas as regras aplicadas coluna a coluna (bronze preservado, ouro limpo)
- Sentinelas por regra: `00000-000`, `000.000.000-00`, `1900-00-00` (decisão de tipo documentada)
- Normalização: telefone `(XX) AAAA-BBBB`, país `Brasil` com mapa de typos, estado com nome completo (27 UFs)
- Auditoria coluna a coluna usando derived table

E a auditoria mostra: 19 estados inválidos e 18 países inválidos. Em 18 linhas ambos ocorrem; em 1 linha só o estado é inválido.

Dado sujo não entra. E quando entra, a gente descobre e documenta.

Case completo (notebook + SQL + notas de decisão): [github.com/renatoapdl/case-tratamento-input](https://github.com/renatoapdl/case-tratamento-input)

---

#EngenhariaDeDados #Databricks #SQL #DataQuality #DataEngineering #Portfolio


## Recomendação

**Comece com a Opção 1**, ajustando para o dia 1 do posicionamento v3. Depois:

- Semana 2: Opção 2 (técnico)
- Semana 3: Opção 3 (pessoal)
- Semana 4: Opção 4 (case pipeline-etl-vendas) - repo no GitHub
- Semana 5+: Opção 5 (case Databricks) - repo no ar

Regras de execução:
1. **Horário:** terça a quinta, 8h–10h ou 18h–20h
2. **Formato:** parágrafos curtos, emojis com moderação
3. **Engajamento:** responder TODOS os comentários nas primeiras 2 horas
4. **Imagem:** foto sua ou print do pipeline (arquitetura do ETL)
5. Todas as hashtags com foco em dados (remove web/fullstack)