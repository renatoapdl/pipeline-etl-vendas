# Contexto Linux e Infraestrutura — material de entrevista

> Fonte: resposta do usuário em 01/10/2026, bloco 1 das perguntas.
> **Regra:** tudo aqui é o que ele realmente faz. Nada foi inferido ou melhorado.
> Se uma resposta de entrevista não estiver neste arquivo, ela não foi confirmada.

---

## 1. AS 4 MÁQUINAS DE OPERAÇÃO (todas Debian)

| Máquina | Função | O que ele faz lá |
|---|---|---|
| **Gravador VLBI** | grava os dados de observação | cria scripts, lê logs, cria diretórios para salvar os dados |
| **Transmissor** | envia os discos gravados do gravador para servidores externos | move os discos do gravador para o transmissor e executa envio por protocolo próprio |
| **Servidor** | hospeda Grafana e HTMLs de uso interno | dashboards acessíveis só na rede interna |
| **PC de operação** | estação de trabalho | baixa arquivo de rede externa com `fetch`, edita arquivos de schedule com `vim` e `nano`, navega diretórios, cria/move/deleta/copia, envia arquivos entre máquinas e diretórios |

Rede: IVS-NASA (Rádio Observatório Espacial do Nordeste).

---

## 2. O DIA TIPO

1. Cria arquivos e diretórios.
2. Envia os arquivos gravados nas sessões VLBI.
3. Edita arquivos de schedule.
4. Roda comandos no **Field System** (programa do VLBI).
5. Se der erro: abre os logs, acha a causa.

---

## 3. COMANDO REAL DE ENVIO DE DADOS

```bash
./m5copy dado -udt -r 600M -p 46225 --resume -t 120
```

Transporte de dados observacionais para servidores externos, por protocolo próprio, com retomada.

### Por que esse comando vale ouro como storytelling de dados

Não é "eu uso Linux". É o conceito de engenharia de dados aparecendo na rotina:

| Flag | O que é | Equivalente em dados |
|---|---|---|
| `-r 600M` | bloco de 600 MB por rodada | **particionamento / lote** |
| `--resume` | retoma do ponto em que parou | **idempotência e checkpoint** |
| `-t 120` | timeout de 120 s por tentativa | **retry com backoff** |
| `-p 46225` | porta do destino | **endpoints e config por ambiente** |
| `-udt` | modo de transporte UDP datagrama | **transporte não confiável, precisa de negócio por cima** |

O ponto que ele deve saber explicar em entrevista: **link de dados não confiável exige idempotência**. Se a conexão cai no meio, o transporte tem que poder recomeçar sem duplicar e sem perder. É o mesmo problema de reprocessar um pipeline que já rodou pela metade, que é a regra R6 do `transform.py`.

Essa é a ponte honesta entre a infraestrutura NASA e engenharia de dados. Não é metáfora: é o mesmo raciocínio.

---

## 4. STACK CONFIRMADA

- Debian (4+ máquinas de operação)
- SSH / MobaXterm
- Shell: `awk`, `sed` já usou. **`crontab` NÃO.**
- `vim` e `nano`
- `fetch` para baixar arquivo de rede externa
- Grafana (hospedado, dashboards internos)
- Alertas em **Telegram e e-mail**
- Field System (software de VLBI)
- Python (automação, ETL)

---

## 5. O QUE ELE **NÃO** FAZ (não afirmar o contrário)

Isto é tão importante quanto a lista do que faz. A vaga DOMO tem checklist de conformidade, e dizer que faz algo que não faz custa caro.

- **Não faz deploy.** Não tem histórico de deploy automatizado.
- **Não usa Docker nem container em produção.** Nada de container nas 4 máquinas.
- **Não usa Kubernetes.**
- **Não fez container orchestration de forma alguma.**
- **Não usa `crontab`.**
- **Não tem anecdote de incidente às 3h confirmado ainda** (pergunta 3 do bloco 1 ficou sem resposta).

Consequência prática: Docker e Kubernetes continuam lacuna, e a resposta certa não é fingir. É o storyline do item 9 do `VAGA_DOMO-MERCANTIL.md`: projeto com Spark + Airflow + Docker mata 3 lacunas de uma vez, e é a semana 5b do plano.

---

## 6. RASCUNHOS DE RESPOSTA PARA ENTREVISTA

Rascunho. Ele precisa ler, corrigir e só então usar. Não está mais bonito do que ele fala de verdade.

### "Fale sobre seu ambiente Linux"

> "Trabalho com 4 máquinas Debian de operação na rede IVS-NASA, e acesso por SSH, geralmente por MobaXterm. Uma é o gravador dos dados de VLBI, onde eu crio scripts e leio logs. Outra é o transmissor, onde movo os discos gravados e executo o envio para servidores externos com um protocolo próprio. Tem um servidor onde hospedo o Grafana e os dashboards, que só a rede interna acessa. E um PC de operação, onde eu baixo arquivos de rede externa, edito os arquivos de schedule no vim e organizo os diretórios e transfers entre máquinas."

### "Como você monitora?"

> "Grafo no Grafana, que eu hospedo num servidor interno. Os alertas chegam por Telegram e e-mail."

### "Me dá um exemplo de comando real"

> "O envio dos dados observacionais para os servidores externos. `./m5copy dado -udt -r 600M -p 46225 --resume -t 120`. O que importa aqui não é a flag, é o `--resume`: o link não é confiável, então o transporte precisa poder retomar de onde parou sem duplicar e sem perder. Isso é idempotência, e é a mesma coisa que eu preciso fazer quando reprocesso um pipeline que rodou pela metade."

### "Você faz deploy?"

Resposta honesta: "No meu trabalho atual, não. Eu opero e monitoro, não faço deploy de aplicação. É uma lacuna que eu estou fechando agora: o projeto de Pipeline de Dados que estou montando tem Docker e Airflow justamente para isso."

Não inventa. Se perguntarem por que não faz, a resposta é a mesma: 14 anos em operação e confiabilidade, agora construindo a parte de orquestração.

---

## 7. PENDÊNCIAS

- [x] Bloco 1 (perguntas 1, 2, 4, 5, 6, 7) — respondido em 01/10/2026
- [ ] **Bloco inteiro restante:** perguntas detalhadas e material de portfólio. Fica em `ENTREVISTA_INFRA_QUESTIONARIO.md`, que ele preenche no tempo dele
- [ ] Pergunta 3 (incidente real), a de maior valor de entrevista, ainda sem resposta
- [ ] Ler e corrigir os rascunhos da seção 6 com a própria fala

Quando ele escrever `vou responder o questionário` ou `respondi o arquivo`, eu leio `ENTREVISTA_INFRA_QUESTIONARIO.md` inteiro e trabalho em cima dele.