# Aula SQLBolt â€” roteiro do professor

> Este arquivo Ã© meu (IA). **Gatilho:** quando ele escrever `vamos iniciar a aula de SQL`, eu leio isto e sigo.
> Objetivo: fechar o gap de SQL relacional (JOIN, GROUP BY, NULL, agregados) e terminar a semana 1 com commit.
> Complemento: `aula_transform_py.md` (mesmo mÃ©todo, mesmo papel).

---

## 0. POR QUE SQLBolt, E O QUE ELE NÃƒO FAZ

Verifiquei a grade no ar. O que ele cobre:

| Aula | Assunto | Cobre nosso gap? |
|---|---|---|
| 1 | `SELECT` 101 | NÃ£o, vocÃª jÃ¡ sabe |
| 2 | Constraints pt 1 (`WHERE`, `<`, `>`, `LIKE`) | JÃ¡ sabe |
| 3 | Constraints pt 2 (`IN`, `BETWEEN`, `IS NULL`) | Sim, `IS NULL` importa |
| 4 | Filtering e sorting (`ORDER BY`, `LIMIT`, `DISTINCT`) | JÃ¡ sabe |
| Review | RevisÃ£o | Pular |
| 6 | **JOINs** | **Sim, Ã© o alvo principal** |
| 7 | **OUTER JOINs** | **Sim** |
| 8 | **Nota sobre NULLs** | **Sim, e Ã© a aula mais relevante dele** |
| 9 | Queries com expressÃµes | Support |
| 10 | Agregados pt 1 (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) | Sim |
| 11 | **GROUP BY e HAVING** | **Sim** |
| 12 | **Ordem de execuÃ§Ã£o da query** | **Sim, e Ã© a que mais cai em entrevista** |
| 13 a 18 | `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, `DROP` | NÃ£o agora |
| TÃ³picos | Subqueries, `UNION`, `INTERSECT`, `EXCEPT` | Depois |

**CorreÃ§Ã£o importante ao plano anterior:** eu disse "SQLBolt â†’ SQLZoo â†’ window functions". SQLBolt **nÃ£o tem window function nem CTE**. Ele resolve JOIN, NULL, GROUP BY/HAVING e ordem de execuÃ§Ã£o. Window function e CTE ficam para a semana 2, escritos por nÃ³s dois sobre os dados dele.

**Link:** https://sqlbolt.com/

Aviso prÃ¡tico: o editor interativo Ã© JavaScript antigo e Ã s vezes nÃ£o carrega em navegador novo. Se a tabela nÃ£o aparecer, o texto da aula e o bloco "Solution" continuam funcionando. NÃ£o trava por causa disso.

Plano realista: aulas 6, 7, 8, 10, 11, 12 hoje e amanhÃ£. Aulas 1 a 5 ele passa rÃ¡pido para calibrar o nÃ­vel. Aulas 13 a 18 ficam para quando ele criar as tabelas dele na semana 2.

---

## 1. O MÃ‰TODO

Igual Ã  aula do transform. Regras que valem aqui:

1. Ele escreve a query. Eu nÃ£o.
2. **Antes de ele rodar**, ele me diz o que espera. Depois roda, e compara. DivergÃªncia vira discussÃ£o.
3. Cada query que ele terminar Ã© **traduzida para o dado dele**. O exercÃ­cio do SQLBolt Ã© absorvido, o commit Ã© a query nos dados dele.
4. Pergunta de porquÃª depois de cada acerto.
5. NÃ­vel de pista igual ao da outra aula: reformulo â†’ conceito â†’ nome da funÃ§Ã£o â†’ esqueleto â†’ linha.

Acrescento uma regra especÃ­fica deste roteiro:

6. **Toda query vai nascendo com uma pergunta de negÃ³cio.** NÃ£o "faÃ§a o exercÃ­cio 2", e sim "vocÃª precisa saber quantas vendas cada canal perdeu, o que vocÃª pergunta?".

Sem pergunta de negÃ³cio, SQL vira exercÃ­cio de sintaxe e nÃ£o fixa.

---

## 2. POR QUE ISSO FECHA UMA LACUNA REAL

Verifiquei os dois projetos:

- `pipeline-etl-vendas`: 100% DataFrame API do PySpark, zero arquivo `.sql`.
- `case-tratamento-input`: tem 4 arquivos `.sql`, e o `03_ouro.sql` sÃ£o 76 linhas de query boa.

O que vocÃª jÃ¡ demonstra em SQL: `CASE WHEN`, `CONTAINS`, `LENGTH`, `CONCAT`, `SUBSTRING`, `TRIM`, `UPPER`, `IN`, `REGEXP_LIKE`, `COUNT_IF`, derived table, `CURRENT_DATE`, `YEAR`.

Isso Ã© **SQL de linha**, que Ã© o que ETL faz. Ã‰ bom e estÃ¡ bem feito.

O que nÃ£o existe em nenhum dos dois projetos, e estÃ¡ tudo em aberto no seu checklist 4.2: `JOIN`, `GROUP BY`, `HAVING`, subquery, CTE, window function.

Traduzindo: seus dois repositÃ³rios sÃ£o projeto de **uma tabela sÃ³**. VocÃª nunca precisou relacionar quatro tabelas nem agregar sobre janelas. Em entrevista de dados jÃºnior isso Ã© pergunta de rotina, e a vaga DOMO lista SQL explicitamente.

Por isso SQL tem precedÃªncia sobre PySpark nesta semana: PySpark window vocÃª jÃ¡ demonstra no pipeline, com `row_number` na deduplicaÃ§Ã£o. SQL relacional Ã© o buraco real.

---

## 3. A PONTE: DO CSV PLANO PARA O MODELO RELACIONAL

Este Ã© o trabalho da semana 2, e Ã© o que faz o SQL deixar de ser exercÃ­cio.

O CSV dele tem 27 linhas e 9 colunas, uma tabela sÃ³. Para treinar JOIN com dado que ele entende, ele mesmo monta duas ou trÃªs tabelas:

```
dimens_cliente   (id_cliente, nome_cliente, uf, ...)
dimens_produto   (id_produto, produto, categoria, ...)
fato_vendas      (id_venda, id_cliente, id_produto, data_venda, ...)
```

O `fato_vendas` vem do CSV que ele jÃ¡ tem. As dimensÃµes ele cria com os dados que jÃ¡ estÃ£o dentro do CSV mais alguns que ele inventa com cara de real, e ele assume que vivem em outro sistema.

Os dois `id_produto` que ele cria sÃ£o `cabo usb` e `SSD 1TB`, que **existem duplicados** no CSV: `"CABO USB"` em VEN-0005 e `"cabo usb"` em VEN-0014. Isso nÃ£o Ã© invenÃ§Ã£o, Ã© um achado. `"SSD 1TB"` tambÃ©m se repete. Serve de link natural entre a dimensÃ£o e o fato, e mostra por que normalizar texto importa quando vocÃª quer relacionar tabelas.

O objetivo nÃ£o Ã© modelagem perfeita. Ã‰ ter duas tabelas que precisam ser juntas para responder uma pergunta de negÃ³cio.

Onde roda: **Databricks CE Free/serverless**, que ele jÃ¡ usou no case. Ã‰ onde ele vai levar as queries adaptadas e onde o `partitionBy` da semana 4 vai nascer. SQLite serve para treinar, mas nÃ£o serve para mostrar no LinkedIn.

---

## 4. CURRÃCULO

### Passo 0 â€” Calibrar o nÃ­vel

Abrir https://sqlbolt.com/ e fazer as aulas 1 a 5 em sequÃªncia, rÃ¡pido, sem parar para discutir.

Motivo: preciso saber em que ponto ele estÃ¡. Se travar na aula 2, o plano muda.

Me diz o resultado: quantas fez sem googlar e onde travou.

### Passo 1 â€” Aula 6: JOIN

Pergunta de negÃ³cio que ele vai traduzir para o dado dele: "quantas vendas houve por cliente?"

Perguntas antes de rodar:

1. "VocÃª tem uma tabela de vendas. O nome do cliente nÃ£o estÃ¡ em lugar nenhum. De onde ele vem?"
2. "O que `JOIN` faz: junta as linhas ou junta as colunas?"
3. "Se um cliente da tabela de clientes nÃ£o comprou nada, ele aparece no seu resultado?"
4. "O que Ã© `ON`? O que acontece se vocÃª trocar por `USING` sem ter o mesmo nome de coluna?"

Entrega: a query do exercÃ­cio, e a mesma pergunta nos dados dele.

Commit da semana 1 comeÃ§a aqui.

### Passo 2 â€” Aula 7: OUTER JOIN

Pergunta de negÃ³cio: "qual cliente nÃ£o comprou nada?"

Perguntas:

1. "Agora o oposto: quero ver quem nÃ£o tem venda, nÃ£o quem tem."
2. "Qual Ã© a diferenÃ§a entre `INNER` e `LEFT`? Quem fica de fora em cada um?"
3. "O que `LEFT JOIN` precisa que `INNER` nÃ£o precisa?"
4. "Se a coluna da tabela da direita for `null`, isso Ã© o mesmo que zero?"

Entrega: query do exercÃ­cio e a contraposta nos dados dele.

Pergunta de por quÃª, e Ã© a central: "no seu `transform.py`, vocÃª preenche `situacao` com `'desconhecida'`. Se em vez disso deixasse `null`, o que um `LEFT JOIN` na frente nÃ£o conseguiria distinguir de 'nÃ£o comprou'?"

### Passo 3 â€” Aula 8: NULL

Esta Ã© a aula que conversa direto com a regra R5 do transform.

Perguntas:

1. "Por que `= NULL` nÃ£o funciona? O que ele faz?"
2. "O que precisa usar, e para que lado da comparaÃ§Ã£o?"
3. "No seu CSV, `situacao` vazia Ã© `null`? E `quantidade` vazia?"
4. "`COALESCE(a, b)` retorna `b` quando `a` Ã© nulo. E quando `a` Ã© string vazia?"
5. "Por que `COUNT(*)` e `COUNT(coluna)` dÃ£o nÃºmeros diferentes?"

Entrega: os trÃªs testes de NULL na tabela dele.

Pergunta de fechamento: "se vocÃª tivesse lido o CSV no `extract.py` deixando o Spark inferir tipo em vez de declarar tudo como texto, o que mudaria aqui?"

### Passo 4 â€” Aulas 10 e 11: agregados, GROUP BY e HAVING

Pergunta de negÃ³cio: "qual categoria gera mais receita, e quanto?"

Perguntas:

1. "VocÃª quer o total por categoria. O que o `GROUP BY` faz com as linhas antes de somar?"
2. "O que `SUM(valor_total)` faz com as linhas de um mesmo grupo?"
3. "JÃ¡ que a receita Ã© soma, por que contar quantidade nÃ£o serve?"
4. "Agora vocÃª quer sÃ³ categoria acima de um valor. `WHERE` resolve? Qual Ã© a diferenÃ§a entre filtrar linha e filtrar grupo?"
5. "Qual dos dois roda primeiro, `WHERE` ou `HAVING`? E a aula 12 responde isso. EntÃ£o por que existem os dois?"

Entrega: uma query de receita por categoria, com `HAVING`.

Commit da semana 1.

### Passo 5 â€” Aula 12: ordem de execuÃ§Ã£o

Aula curta, alto rendimento. Perguntas:

1. "Uma query com `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`. Em que ordem o banco executa?"
2. "Se `WHERE` roda antes do `GROUP BY`, isso muda como vocÃª filtra? DÃ¡ pra filtrar grupo no `WHERE`?"
3. "Se `SELECT` roda por Ãºltimo, por que nÃ£o dÃ¡ pra usar alias dentro do `WHERE`?"
4. "Qual a ordem de escrita no papel?"

Pergunta de entrevista, e essa cai muito: "me dÃ¡ um caso em que filtrar no `WHERE` dÃ¡ resultado diferente de filtrar no `HAVING`."

---

## 5. ENTREGÃVEIS

Fim da semana 1:

1. Pasta `sql/` no `pipeline-etl-vendas`, com uma query por arquivo.
2. Cada query com comentÃ¡rio de duas linhas no topo: a pergunta de negÃ³cio que ela responde e o que ela espera de volta.
3. Todo arquivo executÃ¡vel no Databricks CE.
4. Cada uma com uma pergunta adicional que **nÃ£o** estava no exercÃ­cio do SQLBolt, tirada dos dados dele.

Exemplo do formato esperado:

```
sql/01_receita_por_categoria.sql
sql/02_clientes_sem_compra.sql
sql/03_vendas_por_canal_e_mes.sql
```

Esse Ã© o material do post de 08/10, sem inventar nada.

---

## 6. LOG

| Passo | Data | Status | ObservaÃ§Ã£o |
|---|---|---|---|
| 0 | 01/10/2026 | concluÃ­do | Aulas 1 a 5 concluÃ­das (SELECT, constraints pt 1 e pt 2, filtering/sorting, revisÃ£o). Sem consultar e sem travar. CalibraÃ§Ã£o: o gargalo nÃ£o Ã© sintaxe de SELECT/WHERE, Ã© SQL relacional. **CorreÃ§Ã£o:** eu tinha dito que `= NULL` aparecia na aula 3. NÃ£o aparece. NULL Ã© a aula 8 ("A short note on NULLs"); a aula 3 Ã© de operadores de texto (`LIKE`, `IN`, `NOT IN`, `%`, `_`). Perguntar sobre NULL no passo 3, nÃ£o no passo 0 |
| 1 | 05/10/2026 | concluÃ­do | JOIN (aula 6) â€” primeira vez que ele vai usar o dado dele, nÃ£o a tabela de movies do SQLBolt |
| 2 | 05/10/2026 | concluÃ­do | OUTER JOIN (aula 7) |
| 3 | 05/10/2026 | concluÃ­do | NULL (aula 8) |
| 4 | 05/10/2026 | concluÃ­do | agregados, GROUP BY, HAVING (aulas 10 e 11) |
| 5 | | pendente | ordem de execuÃ§Ã£o (aula 12) |

**Progresso real:** a aula 6 (JOIN) fecha o item mais caro da lista do seu checklist 4.2. A aula 11 (GROUP BY/HAVING) fecha o segundo. window function e CTE ficam para a semana 2, escritos por nÃ³s dois.

---

## 7. COMO A SEMANA 2 USA ISSO

Não é um bloco separado. A semana 2 é a mesma coisa com duas adições:

1. **Window function** (ow_number, ank, lag, sum over) escrito por ele sobre o CSV dele. São as 4 queries do post de 08/10.
2. **O esquema estrela** da seção 3. Duas dimensões, um fato, e os JOINs viram problema de negócio de verdade.

E a partir daí o post de 08/10 tem material: são as queries que ele escreveu, com a pergunta que cada uma responde.

---

## 8. FLASHCARDS — AVALIAÇÃO E EVOLUÇÃO

### 8.1 Critério de avaliação

Avalie cada resposta em 3 dimensões (0–10):

| Critério | O que avalio | Peso |
|---|---|---|
| Correto | Acertou o conceito | 40% |
| Clareza | Explicou com palavras simples | 40% |
| Exemplo | Usou exemplo prático | 20% |

**Nota da pergunta** = (Correto × 0.40 + Clareza × 0.40 + Exemplo × 0.20)  
**Nota da aula (AVG)** = média das perguntas da aula  
**AVG geral** = média simples por aula

### 8.2 Flashcards por aula

#### A1. Aulas 1–5 (SELECT, WHERE, ORDER BY, DISTINCT, funções)
| # | Pergunta | Resposta esperada | Dificuldade |
|---|---|---|---|
| 1.1 | SELECT vs FROM: O que cada um define numa query? | FROM define a origem. SELECT define o que exibe. Ordem lógica difere da escrita. | Fácil |
| 1.2 | WHERE vs HAVING: Quando filtram? | WHERE filtra linhas antes do GROUP BY. HAVING filtra grupos depois. | Médio |
| 1.3 | ORDER BY: ASC e DESC? | Ordena resultado. ASC padrão (crescente). DESC decrescente. | Fácil |
| 1.4 | DISTINCT: Quando usar? | Remove linhas duplicadas inteiras no resultado. | Fácil |
| 1.5 | LIKE vs IN: Diferença? | IN = igualdade exata. LIKE = padrão com % e _. | Médio |
| 1.6 | Trim/lower no agrupamento: Por quê? | Evita "Notebook" e "notebook" serem tratados como diferentes. | Médio |

**Repetição #__ | Data: __/__/____ | AVG Aula 1–5: __.__ / 10**

#### A2. Aula 6 (JOIN)
| # | Pergunta | Resposta esperada | Dificuldade |
|---|---|---|---|
| 6.1 | JOIN junta linhas ou colunas? | Junta linhas com base em chave. Adiciona colunas da outra tabela. | Médio |
| 6.2 | INNER vs LEFT JOIN: Diferença? | INNER traz só matches. LEFT traz todas da esquerda + NULL quando sem match. | Médio |
| 6.3 | Quando usar LEFT JOIN? | Quando quero preservar o conjunto principal (ex.: todas as vendas). | Médio-Alto |
| 6.4 | Chave de JOIN: Importância? | Garante corretude. Evita duplicações. | Médio |
| 6.5 | Duplicação em JOIN: Quando acontece? | Quando direita tem >1 linha por chave. Resolver com agregação/janela. | Alto |

**Repetição #__ | Data: __/__/____ | AVG Aula 6: __.__ / 10**

#### A3. Aula 7 (OUTER JOINs)
| # | Pergunta | Resposta esperada | Dificuldade |
|---|---|---|---|
| 7.1 | LEFT/RIGHT/FULL: Diferença? | LEFT preserva esquerda. RIGHT direita. FULL ambas. | Médio |
| 7.2 | Quando usar FULL OUTER? | Para achar registros órfãos (auditoria). | Médio-Alto |
| 7.3 | Identificar órfãos? | LEFT com NULL na direita = órfão da direita. | Médio |
| 7.4 | RIGHT → LEFT: Possível? | Sim. Inverter ordem das tabelas. | Médio |
| 7.5 | Quando NÃO usar OUTER? | Quando só importa correspondência (INNER). | Médio |

**Repetição #__ | Data: __/__/____ | AVG Aula 7: __.__ / 10**

#### A4. Aula 8 (NULL)
| # | Pergunta | Resposta esperada | Dificuldade |
|---|---|---|---|
| 8.1 | NULL = 0 ou vazio? | Nenhum. Significa desconhecido. NULL = NULL dá UNKNOWN. | Alto |
| 8.2 | Como testar NULL? | IS NULL / IS NOT NULL. Nunca = NULL. | Fácil |
| 8.3 | NULL em WHERE: Comporta-se como? | Não passa em = nem !=. WHERE exige TRUE. | Alto |
| 8.4 | NOT IN com NULL: Perigo? | Pode retornar vazio se lista contém NULL. | Alto |
| 8.5 | NULL vs "" no ETL? | NULL = "não sei". "" = informado mas vazio. Justifica R5. | Alto |

**Repetição #__ | Data: __/__/____ | AVG Aula 8: __.__ / 10**

#### A5. Aulas 10–11 (GROUP BY, HAVING, Agregados)
| # | Pergunta | Resposta esperada | Dificuldade |
|---|---|---|---|
| 10.1 | GROUP BY: O que faz? | Agrupa linhas com mesmos valores. Aplica agregados por grupo. | Médio |
| 10.2 | O que pode ir no SELECT com GROUP BY? | Só colunas do GROUP BY ou funções agregadas. | Alto |
| 10.3 | COUNT(*) vs COUNT(coluna)? | COUNT(*) conta tudo. COUNT(coluna) ignora NULL. | Médio-Alto |
| 10.4 | WHERE vs HAVING: Ordem e alvo? | WHERE antes (linhas). HAVING depois (grupos). HAVING aceita agregados. | Alto |
| 10.5 | Exemplo prático WHERE vs HAVING? | WHERE filtra linha (quantidade > 1). HAVING filtra grupo (SUM > 10k). | Alto |

**Repetição #__ | Data: __/__/____ | AVG Aulas 10–11: __.__ / 10**

### 8.3 Histórico de repetições

| Aula | Repetição # | Data | AVG (0–10) | Tendência | Foco de reforço |
|---|---|---|---|---|---|
| Aulas 1–5 | 1 | __/__/____ | __._ | ___ | __________________ |
| Aula 6 (JOIN) | 1 | __/__/____ | __._ | ___ | __________________ |
| Aula 7 (OUTER) | 1 | __/__/____ | __._ | ___ | __________________ |
| Aula 8 (NULL) | 1 | __/__/____ | __._ | ___ | __________________ |
| Aulas 10–11 (GROUP BY/HAVING) | 1 | __/__/____ | __._ | ___ | __________________ |
| Aula 12 (Execução) | 1 | __/__/____ | __._ | ___ | __________________ |

**AVG GERAL (Repetição 1):** __.__ / 10