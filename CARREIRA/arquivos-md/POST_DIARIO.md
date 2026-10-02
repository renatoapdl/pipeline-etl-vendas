# POST DIÁRIO (LinkedIn)

## O que este arquivo é

Um arquivo só, com duas partes: as regras (para qualquer modelo que abrir) e o post pronto (para eu copiar e colar no LinkedIn).

Quando eu disser "projeto X pronto, atualiza o post diário" (ou qualquer frase do tipo), o modelo deve:

1. Ler as regras deste arquivo.
2. Ler o projeto (README, notas, saída de execução) e pegar só fatos verificáveis.
3. Reescrever a seção **POST ATUAL** com o projeto novo, seguindo as regras.
4. Me entregar o texto e dizer qual imagem anexar e quais competências associar.

## Regras do post

- **Post de LinkedIn, não markdown.** Sem `**`, sem crase, sem `[texto](url)`, sem títulos com `#`. URL vai solta no final, sem prefixo, para o LinkedIn virar link com preview. Hashtag é a única exceção que o LinkedIn entende.
- **Nada inventado.** Só números, decisões e afirmações que estão no projeto. Nada de estimativa, anecdote ou número "que devia ser". Se um dado não estiver no projeto, não entra.
- **Humanizado.** Aplicar a skill `humanizer` (C:\Users\renat\.agents\skills\humanizer). Sem travessão, sem "não X, mas Y", sem apócrifo, sem frase de efeito no fim, sem lista com rótulo em negrito. Frases de comprimento variado.
- **Serve como case para recrutador.** O leitor tem 3 segundos antes do "... ver mais". A primeira linha tem que dizer o que foi feito e com o quê.
- **3 a 5 hashtags**, no fim, as que o LinkedIn recomenda.
- **Um fato concreto por bullet.** Nada de "várias melhorias", "qualidade de dados", "boas práticas".
- **Tamanho:** até ~1.300 caracteres. Acima disso o post vira artigo.

## Estrutura esperada

1. Primeira linha: projeto + núcleo técnico (ex.: "Case Databricks: do bronze ao ouro em uma única consulta SQL").
2. Uma ou duas frases de contexto: de onde veio o problema (desafio real, trabalho, estudo).
3. O problema em uma frase, com a sujeira concreta.
4. O que foi entregue, em 3 a 5 bullets.
5. Um resultado ou achado com número.
6. Link do repositório (URL solta).
7. Hashtags.

## Depois de publicar

- Anexar o print (imagem 16:9, sem texto pequeno).
- Associar as competências no menu do projeto do LinkedIn: as que o modelo listar junto com o post.

---

## POST ATUAL (copiar daqui até a linha "fim do post")

Case Databricks: do bronze ao ouro em uma única consulta SQL

Montei um case de tratamento de dados em Databricks SQL a partir de um desafio real de processo seletivo.

O problema: 40 registros cheios de sujeira de qualidade de dado.

- idades negativas, emails sem @, datas impossíveis (mês 15, dia 40)
- CPF com letras, salários e dívidas negativos
- estado InvalidState e país grafado errado

O desafio pedia 13 regras de negócio em uma única consulta SQL.

O que eu entreguei:
- um SELECT com todas as regras aplicadas coluna a coluna (bronze preservado, ouro limpo)
- sentinelas por regra: 00000-000, 000.000.000-00, 1900-00-00 (decisão de tipo documentada)
- normalização de telefone (XX) AAAA-BBBB, país Brasil com mapa de typos e nome completo do estado (27 UFs)
- auditoria coluna a coluna com derived table

A auditoria fechou em 19 estados inválidos e 18 países inválidos: 18 linhas com os dois, 1 linha só com o estado inválido.

Dado sujo não entra, e quando entra a gente descobre e documenta.

Notebook, SQL e notas de decisão:
https://github.com/renatoapdl/case-tratamento-input

#EngenhariaDeDados #Databricks #SQL #DataQuality #DataEngineering

fim do post

---

## Material do post atual

- Repositório: `PROJETOS\DATABRICKS` (README, `notas_candidato.md`, `do-bronze-ao-ouro.py`, `sql\01..04`)
- Imagem sugerida: `PROJETOS\DATABRICKS\imagens\print_auditoria.png` (604x405). Alternativa: `print_ouro_1.png` a `print_ouro_4.png`.
- Competências para associar: Azure Databricks · Apache Spark · Spark SQL · SQL · Data Quality · Data Validation · Data Cleansing · ETL · Data Engineering
- Versão com markdown deste mesmo post: `PROJETOS\DATABRICKS\POST_LINKEDIN.md`


## Status do Post Atual: POSTADO - 01/10/2026: 09:00AM
 - Mudar este status para 'PENDENTE' quando o usuário pedir para atualizar o post diário