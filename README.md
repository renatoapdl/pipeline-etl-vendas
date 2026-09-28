# ETL de vendas: CSV → Parquet → Parquet tratado

Pipeline de dados em PySpark: lê um CSV sujo, grava o bruto em Parquet, limpa e transforma, e grava
o resultado em Parquet.

235 linhas de código (sem testes), 9 testes, roda em cerca de 15 segundos.

Os dados são sintéticos e estão versionados em `dados/vendas_bruto.csv`, com sujeira proposital para
cada regra do pipeline ter um motivo de existir.

## Como rodar

Precisa de Python 3.9+ e Java 11+.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

python etl/run.py               # o pipeline inteiro
python -m pytest tests -q       # os testes
```

Saída esperada:

```
[1] extraido: 27 linhas de vendas_bruto.csv

[2] bruto gravado em data\bruto\vendas

    R1 descartadas sem id ou data     27 ->  25
    R2 datas convertidas              25 ->  25
    R3 valores convertidos            25 ->  25
    R4 texto normalizado              25 ->  25
    R5 nulos preenchidos              25 ->  25
    R6 duplicadas removidas           25 ->  23
    D1 valor total criado             23 ->  23

[3] tratada: 23 linhas
    ATENCAO: 1 venda(s) sem valor_unitario; valor_total fica nulo

[4] tratado gravado em data\tratado\vendas
```

## O que acontece

```
dados/vendas_bruto.csv
        │
        ▼
   ┌─────────┐   lê o CSV como texto, sem corrigir nada
   │ extract │   (schema declarado, tudo como string)
   └────┬────┘
        ▼
  data/bruto/vendas      ← Parquet como o dado chegou
        │
        ▼
   ┌───────────┐  6 regras, uma função cada
   │ transform │  descartar, datas, valores, texto, nulos, duplicadas
   └─────┬─────┘  + 1 campo derivado (valor_total)
         ▼
  data/tratado/vendas   ← Parquet limpo, tipado, sem duplicata
```

O bruto é gravado antes de limpar, de propósito: dá para conferir o que mudou comparando os dois
Parquet, e o dado original não se perde.

## A sujeira do CSV e a regra que existe por causa dela

| O que tem no CSV | Regra | O que faz |
|------------------|-------|-----------|
| `189,90` e `R$ 1.234,56` | R3 converter valores | tira o `R$`, remove o ponto de milhar, troca a vírgula por ponto e vira `double` |
| `2026-01-05` e `17/02/2026` | R2 padronizar datas | as duas viram `date` |
| `  Notebook  `, `CABO USB`, `CANCELADO` | R4 normalizar texto | `trim` + `lower`, para o agrupamento não quebrar |
| `quantidade` e `situacao` vazias | R5 preencher nulos | quantidade vira 1; situação vira `desconhecida` |
| `VEN-0004` e `VEN-0011` aparecem 2 vezes | R6 remover duplicadas | `row_number` por `id_venda` ordenado por data, fica a mais recente |
| 1 linha sem `id_venda` e 1 sem `data_venda` | R1 descartar incompletos | sai do resultado e aparece na contagem do log |
| 1 linha sem preço | nenhuma | fica nulo de propósito, e o log avisa (ver abaixo) |
| campo vazio | nenhuma | o Spark lê como `null`, não como texto vazio |

Resultado: 27 linhas entram, 23 saem. Nenhum `id_venda` repetido, nenhuma data nula.

## Quatro bugs que só apareceram ao rodar

1. `189.90` virou `18990.0`. A primeira versão do CSV tinha valores em dois formatos e a regra
   tratava ponto como separador de milhar. O resultado estava 100× errado, porque o `count()`
   continuava 23. Corrigi padronizando a entrada em formato brasileiro: o número depende do sistema
   de origem.
2. A regra de situação vazia checava texto vazio (`""`), e o CSV entrega `null`. O teste montava o
   DataFrame com `""` e passava; o pipeline real deixava `situacao` nula. O teste virou parametrizado
   (`null` e `""`) e a regra passou a checar os dois.
3. `to_date` não aceita lista de formatos no PySpark 3.5 (`Method to_date([Column, ArrayList]) does
   not exist`). Resolvido com `when` escolhendo o formato antes de converter.
4. `Python worker failed to connect back` nos 7 testes. O worker do Spark sobe o `python` que estiver
   no PATH, e na minha máquina era um Python 3.14 sem o PySpark. Resolvido apontando `PYSPARK_PYTHON`
   para o mesmo interpretador do driver.

## Decisões que eu tomei, e por quê

- Schema declarado com tudo como `string`. Se eu deixasse o Spark inferir, `valor_unitario` viraria
  `string` numa linha e `double` na outra, porque o arquivo mistura formatos. Lendo tudo como texto, a
  conversão acontece num lugar só, de propósito.
- Nem todo nulo é preenchido. `quantidade` vazia é 1. Já preço vazio continua nulo: inventar 0 ou 1
  distorceria o faturamento. O log avisa e a decisão fica com quem lê.
- Modo `overwrite` na gravação, o que torna a execução idempotente: rodar duas vezes não duplica
  linha. Reprocessar é seguro.
- Sem particionamento por data. Com 23 linhas seria enfeite. Serve aqui para mostrar o conceito; num
  volume real, `partitionBy("data_venda")` é o que evita varrer tudo a cada consulta.
- `valor_total` é o campo derivado, calculado a partir de dois campos de origem.

## Arquivos

| Arquivo | Linhas | O que é |
|---------|--------|---------|
| `etl/extract.py` | 35 | lê o CSV, com schema declarado |
| `etl/transform.py` | 107 | as 6 regras + o campo derivado |
| `etl/load.py` | 18 | grava Parquet |
| `etl/run.py` | 75 | executa o pipeline e mostra o efeito de cada regra |
| `tests/test_transform.py` | 115 | 9 testes, um por regra e dois de borda |

## Testes

```
9 passed
```

Cobrem: valor com moeda e vírgula, data em `dd/mm/aaaa`, texto com espaço e caixa alta, duplicada
mantendo a data mais recente, nulo como `null` e como `""`, campo derivado, linha sem id/data, e o
preço ausente continuar nulo.

No Windows, se aparecer `Python worker failed to connect back`, é o motivo do `PYSPARK_PYTHON` explicado
acima. Se faltar o `winutils.exe`, o PySpark no Windows precisa do Hadoop: aponte `HADOOP_HOME` para uma
pasta que contenha `bin\winutils.exe`.

## O que não tem aqui

Não tem orquestração (Airflow), quality gate com bloqueio de publicação, particionamento, Delta Lake,
Kubernetes, nem carga em warehouse.

Se subir um degrau, a ordem seria: quality gate que reprova a publicação → particionamento por data →
DAG no Airflow → escrita em Delta.
