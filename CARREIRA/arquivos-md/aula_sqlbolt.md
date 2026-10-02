# Aula SQLBolt — roteiro do professor

> Este arquivo é meu (IA). **Gatilho:** quando ele escrever `vamos iniciar a aula de SQL`, eu leio isto e sigo.
> Objetivo: fechar o gap de SQL relacional (JOIN, GROUP BY, NULL, agregados) e terminar a semana 1 com commit.
> Complemento: `aula_transform_py.md` (mesmo método, mesmo papel).

---

## 0. POR QUE SQLBolt, E O QUE ELE NÃO FAZ

Verifiquei a grade no ar. O que ele cobre:

| Aula | Assunto | Cobre nosso gap? |
|---|---|---|
| 1 | `SELECT` 101 | Não, você já sabe |
| 2 | Constraints pt 1 (`WHERE`, `<`, `>`, `LIKE`) | Já sabe |
| 3 | Constraints pt 2 (`IN`, `BETWEEN`, `IS NULL`) | Sim, `IS NULL` importa |
| 4 | Filtering e sorting (`ORDER BY`, `LIMIT`, `DISTINCT`) | Já sabe |
| Review | Revisão | Pular |
| 6 | **JOINs** | **Sim, é o alvo principal** |
| 7 | **OUTER JOINs** | **Sim** |
| 8 | **Nota sobre NULLs** | **Sim, e é a aula mais relevante dele** |
| 9 | Queries com expressões | Support |
| 10 | Agregados pt 1 (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) | Sim |
| 11 | **GROUP BY e HAVING** | **Sim** |
| 12 | **Ordem de execução da query** | **Sim, e é a que mais cai em entrevista** |
| 13 a 18 | `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, `DROP` | Não agora |
| Tópicos | Subqueries, `UNION`, `INTERSECT`, `EXCEPT` | Depois |

**Correção importante ao plano anterior:** eu disse "SQLBolt → SQLZoo → window functions". SQLBolt **não tem window function nem CTE**. Ele resolve JOIN, NULL, GROUP BY/HAVING e ordem de execução. Window function e CTE ficam para a semana 2, escritos por nós dois sobre os dados dele.

**Link:** https://sqlbolt.com/

Aviso prático: o editor interativo é JavaScript antigo e às vezes não carrega em navegador novo. Se a tabela não aparecer, o texto da aula e o bloco "Solution" continuam funcionando. Não trava por causa disso.

Plano realista: aulas 6, 7, 8, 10, 11, 12 hoje e amanhã. Aulas 1 a 5 ele passa rápido para calibrar o nível. Aulas 13 a 18 ficam para quando ele criar as tabelas dele na semana 2.

---

## 1. O MÉTODO

Igual à aula do transform. Regras que valem aqui:

1. Ele escreve a query. Eu não.
2. **Antes de ele rodar**, ele me diz o que espera. Depois roda, e compara. Divergência vira discussão.
3. Cada query que ele terminar é **traduzida para o dado dele**. O exercício do SQLBolt é absorvido, o commit é a query nos dados dele.
4. Pergunta de porquê depois de cada acerto.
5. Nível de pista igual ao da outra aula: reformulo → conceito → nome da função → esqueleto → linha.

Acrescento uma regra específica deste roteiro:

6. **Toda query vai nascendo com uma pergunta de negócio.** Não "faça o exercício 2", e sim "você precisa saber quantas vendas cada canal perdeu, o que você pergunta?".

Sem pergunta de negócio, SQL vira exercício de sintaxe e não fixa.

---

## 2. POR QUE ISSO FECHA UMA LACUNA REAL

Verifiquei os dois projetos:

- `pipeline-etl-vendas`: 100% DataFrame API do PySpark, zero arquivo `.sql`.
- `case-tratamento-input`: tem 4 arquivos `.sql`, e o `03_ouro.sql` são 76 linhas de query boa.

O que você já demonstra em SQL: `CASE WHEN`, `CONTAINS`, `LENGTH`, `CONCAT`, `SUBSTRING`, `TRIM`, `UPPER`, `IN`, `REGEXP_LIKE`, `COUNT_IF`, derived table, `CURRENT_DATE`, `YEAR`.

Isso é **SQL de linha**, que é o que ETL faz. É bom e está bem feito.

O que não existe em nenhum dos dois projetos, e está tudo em aberto no seu checklist 4.2: `JOIN`, `GROUP BY`, `HAVING`, subquery, CTE, window function.

Traduzindo: seus dois repositórios são projeto de **uma tabela só**. Você nunca precisou relacionar quatro tabelas nem agregar sobre janelas. Em entrevista de dados júnior isso é pergunta de rotina, e a vaga DOMO lista SQL explicitamente.

Por isso SQL tem precedência sobre PySpark nesta semana: PySpark window você já demonstra no pipeline, com `row_number` na deduplicação. SQL relacional é o buraco real.

---

## 3. A PONTE: DO CSV PLANO PARA O MODELO RELACIONAL

Este é o trabalho da semana 2, e é o que faz o SQL deixar de ser exercício.

O CSV dele tem 27 linhas e 9 colunas, uma tabela só. Para treinar JOIN com dado que ele entende, ele mesmo monta duas ou três tabelas:

```
dimens_cliente   (id_cliente, nome_cliente, uf, ...)
dimens_produto   (id_produto, produto, categoria, ...)
fato_vendas      (id_venda, id_cliente, id_produto, data_venda, ...)
```

O `fato_vendas` vem do CSV que ele já tem. As dimensões ele cria com os dados que já estão dentro do CSV mais alguns que ele inventa com cara de real, e ele assume que vivem em outro sistema.

Os dois `id_produto` que ele cria são `cabo usb` e `SSD 1TB`, que **existem duplicados** no CSV: `"CABO USB"` em VEN-0005 e `"cabo usb"` em VEN-0014. Isso não é invenção, é um achado. `"SSD 1TB"` também se repete. Serve de link natural entre a dimensão e o fato, e mostra por que normalizar texto importa quando você quer relacionar tabelas.

O objetivo não é modelagem perfeita. É ter duas tabelas que precisam ser juntas para responder uma pergunta de negócio.

Onde roda: **Databricks CE Free/serverless**, que ele já usou no case. É onde ele vai levar as queries adaptadas e onde o `partitionBy` da semana 4 vai nascer. SQLite serve para treinar, mas não serve para mostrar no LinkedIn.

---

## 4. CURRÍCULO

### Passo 0 — Calibrar o nível

Abrir https://sqlbolt.com/ e fazer as aulas 1 a 5 em sequência, rápido, sem parar para discutir.

Motivo: preciso saber em que ponto ele está. Se travar na aula 2, o plano muda.

Me diz o resultado: quantas fez sem googlar e onde travou.

### Passo 1 — Aula 6: JOIN

Pergunta de negócio que ele vai traduzir para o dado dele: "quantas vendas houve por cliente?"

Perguntas antes de rodar:

1. "Você tem uma tabela de vendas. O nome do cliente não está em lugar nenhum. De onde ele vem?"
2. "O que `JOIN` faz: junta as linhas ou junta as colunas?"
3. "Se um cliente da tabela de clientes não comprou nada, ele aparece no seu resultado?"
4. "O que é `ON`? O que acontece se você trocar por `USING` sem ter o mesmo nome de coluna?"

Entrega: a query do exercício, e a mesma pergunta nos dados dele.

Commit da semana 1 começa aqui.

### Passo 2 — Aula 7: OUTER JOIN

Pergunta de negócio: "qual cliente não comprou nada?"

Perguntas:

1. "Agora o oposto: quero ver quem não tem venda, não quem tem."
2. "Qual é a diferença entre `INNER` e `LEFT`? Quem fica de fora em cada um?"
3. "O que `LEFT JOIN` precisa que `INNER` não precisa?"
4. "Se a coluna da tabela da direita for `null`, isso é o mesmo que zero?"

Entrega: query do exercício e a contraposta nos dados dele.

Pergunta de por quê, e é a central: "no seu `transform.py`, você preenche `situacao` com `'desconhecida'`. Se em vez disso deixasse `null`, o que um `LEFT JOIN` na frente não conseguiria distinguir de 'não comprou'?"

### Passo 3 — Aula 8: NULL

Esta é a aula que conversa direto com a regra R5 do transform.

Perguntas:

1. "Por que `= NULL` não funciona? O que ele faz?"
2. "O que precisa usar, e para que lado da comparação?"
3. "No seu CSV, `situacao` vazia é `null`? E `quantidade` vazia?"
4. "`COALESCE(a, b)` retorna `b` quando `a` é nulo. E quando `a` é string vazia?"
5. "Por que `COUNT(*)` e `COUNT(coluna)` dão números diferentes?"

Entrega: os três testes de NULL na tabela dele.

Pergunta de fechamento: "se você tivesse lido o CSV no `extract.py` deixando o Spark inferir tipo em vez de declarar tudo como texto, o que mudaria aqui?"

### Passo 4 — Aulas 10 e 11: agregados, GROUP BY e HAVING

Pergunta de negócio: "qual categoria gera mais receita, e quanto?"

Perguntas:

1. "Você quer o total por categoria. O que o `GROUP BY` faz com as linhas antes de somar?"
2. "O que `SUM(valor_total)` faz com as linhas de um mesmo grupo?"
3. "Já que a receita é soma, por que contar quantidade não serve?"
4. "Agora você quer só categoria acima de um valor. `WHERE` resolve? Qual é a diferença entre filtrar linha e filtrar grupo?"
5. "Qual dos dois roda primeiro, `WHERE` ou `HAVING`? E a aula 12 responde isso. Então por que existem os dois?"

Entrega: uma query de receita por categoria, com `HAVING`.

Commit da semana 1.

### Passo 5 — Aula 12: ordem de execução

Aula curta, alto rendimento. Perguntas:

1. "Uma query com `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`. Em que ordem o banco executa?"
2. "Se `WHERE` roda antes do `GROUP BY`, isso muda como você filtra? Dá pra filtrar grupo no `WHERE`?"
3. "Se `SELECT` roda por último, por que não dá pra usar alias dentro do `WHERE`?"
4. "Qual a ordem de escrita no papel?"

Pergunta de entrevista, e essa cai muito: "me dá um caso em que filtrar no `WHERE` dá resultado diferente de filtrar no `HAVING`."

---

## 5. ENTREGÁVEIS

Fim da semana 1:

1. Pasta `sql/` no `pipeline-etl-vendas`, com uma query por arquivo.
2. Cada query com comentário de duas linhas no topo: a pergunta de negócio que ela responde e o que ela espera de volta.
3. Todo arquivo executável no Databricks CE.
4. Cada uma com uma pergunta adicional que **não** estava no exercício do SQLBolt, tirada dos dados dele.

Exemplo do formato esperado:

```
sql/01_receita_por_categoria.sql
sql/02_clientes_sem_compra.sql
sql/03_vendas_por_canal_e_mes.sql
```

Esse é o material do post de 08/10, sem inventar nada.

---

## 6. LOG

| Passo | Data | Status | Observação |
|---|---|---|---|
| 0 | 01/10/2026 | concluído | Aulas 1 a 5 concluídas (SELECT, constraints pt 1 e pt 2, filtering/sorting, revisão). Sem consultar e sem travar. Calibração: o gargalo não é sintaxe de SELECT/WHERE, é SQL relacional. **Correção:** eu tinha dito que `= NULL` aparecia na aula 3. Não aparece. NULL é a aula 8 ("A short note on NULLs"); a aula 3 é de operadores de texto (`LIKE`, `IN`, `NOT IN`, `%`, `_`). Perguntar sobre NULL no passo 3, não no passo 0 |
| 1 | | pendente | JOIN (aula 6) — primeira vez que ele vai usar o dado dele, não a tabela de movies do SQLBolt |
| 2 | | pendente | OUTER JOIN (aula 7) |
| 3 | | pendente | NULL (aula 8) |
| 4 | | pendente | agregados, GROUP BY, HAVING (aulas 10 e 11) |
| 5 | | pendente | ordem de execução (aula 12) |

**Progresso real:** a aula 6 (JOIN) fecha o item mais caro da lista do seu checklist 4.2. A aula 11 (GROUP BY/HAVING) fecha o segundo. window function e CTE ficam para a semana 2, escritos por nós dois.

---

## 7. COMO A SEMANA 2 USA ISSO

Não é um bloco separado. A semana 2 é a mesma coisa com duas additions:

1. **Window function** (`row_number`, `rank`, `lag`, `sum over`) escrito por ele sobre o CSV dele. São as 4 queries do post de 08/10.
2. **O esquema estrela** da seção 3. Duas dimensões, um fato, e os JOINs viram problema de negócio de verdade.

E a partir daí o post de 08/10 tem material: são as queries que ele escreveu, com a pergunta que cada uma responde.
