# Questionário de entrevista — Linux e infraestrutura

> **Gatilho para mim (IA):** quando ele escrever algo como `vou responder o questionário`, `respondi o arquivo` ou `voltei pro questionário`, eu leio este arquivo inteiro e trabalho em cima dele.
> Origem: perguntas que fiz em 01/10/2026 para levantar material de entrevista e montar a skill de Linux.
> Arquivo companheiro: `CONTEXTO_LINUX_INFRA.md` (o que já está confirmado e as respostas rascunhadas).

---

## COMO USAR ESTE ARQUIVO

Responda aqui, no seu tempo, quantas vezes quiser. Não precisa escrever bonito, não precisa saber o termo técnico.

**O fluxo quando você não sabe o nome técnico:** em vez de tentar escrever a resposta aqui, me descreve o que você faz em português, do jeito que sai. Eu te devolvo três ou quatro termos técnicos que descrevem aquela mesma coisa, com o que cada um significa e quando usar. Você escolhe e escreve aqui.

Regra que vale sempre: **só adota um termo técnico se souber explicar por que ele se aplica.** Termo decorado quebra na segunda pergunta de follow-up. O objetivo não é parecer especialista, é não travar.

Para eu te ajudar melhor, em cada resposta tenta dizer:

- **o que você queria que acontecesse**
- **o que aconteceu**
- **o que você fez para descobrir**
- **o que você mudou**

---

## BLOCO 1 — ambiente e rotina (7 perguntas)

### 1. Quais são as máquinas? Qual a função de cada uma?

**Respondido.** Debian, 4 máquinas de operação na rede IVS-NASA:

- **Gravador VLBI:** cria scripts, lê logs, cria diretórios para salvar os dados.
- **Transmissor:** move os discos gravados do gravador para o transmissor e envia para servidores externos por protocolo próprio.
- **Servidor:** hospeda Grafana e HTMLs, acessados só pela rede interna.
- **PC de operação:** baixa arquivo de rede externa com `fetch`, edita arquivos de schedule com `vim` e `nano`, navega diretórios, cria/move/deleta/copia arquivos, envia arquivos entre máquinas e diretórios.

**Conceitos que isso demonstra** (sugestões minhas, confirme):

| O que você faz | Termo técnico |
|---|---|
| 4 máquinas com papéis distintos e rodando | ambiente multi-host / topologia de rede |
| acesso remoto por SSH | administração remota |
| criar diretórios e decidir onde salvar | organização de armazenamento, convenção de paths |
| mover disco do gravador para o transmissor | **fluxo de dados entre etapas (handoff)** |
|iso dados para servidor externo | **ingestão / egress de dados** |
| Grafana em servidor interno | observabilidade e monitoramento |
| vim/nano em arquivos de schedule | configuração como código (mesmo que manual) |

> **Pendente para você:** alguma dessas 4 já esteve fora do ar? Alguma delas é crítica e não pode cair? Se uma delas cair, o que para de funcionar? Isso responde direto a pergunta de disponibilidade que a vaga DOMO faz.

### 2. O que você faz num dia comum?

**Respondido.**

1. Cria arquivos e diretórios.
2. Envia os arquivos gravados nas sessões VLBI.
3. Edita arquivos de schedule.
4. Roda comandos no Field System.
5. Se der erro: abre os logs, acha a causa.

**Conceitos:** rotina operacional, execução de procedimento, troubleshooting por log, leitura de erro.

> **Pendente:** com que frequência? Isso é todo dia, ou tem sessão de observação em turnos? E tem horário fixo, tipo agendado por cron, ou você dispara na mão?

### 3. Já precisou investigar um incidente? Conta o que aconteceu, como descobriu e o que fez.

**NÃO RESPONDIDO. Esta é a pergunta mais importante do questionário.**

É a que separa quem só estudou de quem operou. Não precisa ser desastre. Serve qualquer erro que você teve que rastrear até a causa, desde que você consiga explicar o que era e por que era.

Para destravar, responde o que tiver de mais próximo:

1. Qual foi o erro mais difícil que você já resolveu no Field System ou nos scripts? Não precisa ser o mais importante, precisa ser o que você mais lembra.
2. Qual foi a mensagem de erro, ou como ela se manifestou? (crash, arquivo vazio, dado errado, envio que falhou)
3. Como você descobriu? Leu log, viu alerta no Grafana, percebeu que o arquivo não chegou, alguém avisou?
4. O que você procurou primeiro no log?
5. Qual era a causa?
6. O que você fez para resolver?
7. O que você mudou para não repetir?
8. Alguém já tinha acontecido antes? Como você soube?

Se a resposta for "nunca tive incidente":

Diz isso. Aí eu construo a pergunta de outro jeito, com o erro mais chato do dia a dia, que tem o mesmo valor de entrevista. Erro recorrente é incidente.

### 4. Já fez deploy? Ou só monitora? Tem `systemctl`, gerenciador, Ansible?

**Respondido:** não faz deploy, não que lembre. Monitora e opera.

**Conceito a levar:** ele está no lado de **operação e confiabilidade**, não de entrega contínua. Isso é coerente com os 14 anos em infraestrutura crítica.

> **Pendente e importante:** mesmo sem deploy, existe alguma coisa que você **sobe no ar**? Tipo: um HTML novo no servidor, um dashboard novo, um script novo, um serviço que você inicia. Se existe, isso é deploy e vale contar. Existe?

### 5. Onde guardam os arquivos? Tem banco rodando? Tem container? Tem Docker em produção?

**Respondido:** sem container e sem Docker nas máquinas de operação.

**Pendnete:** tem algum banco de dados rodando em alguma dessas máquinas? Banco, planilha em CSV, nada? Tem backup? Onde fica o backup? Se a máquina morre, o que ainda existe?

### 6. Já escreveu script shell? `awk`, `sed`, `crontab`?

**Respondido:** já escreveu shell, usou `awk` e `sed`. `crontab` não.

**Pendente:** o que o script fazia? Onde ele roda (local ou remoto)? Tem algum script rodando sozinho, ou você sempre executa na mão? E `awk` e `sed` foram em arquivo de log, em CSV, ou transformation de texto?

### 7. Como você monitora? Como um alerta chega até você?

**Respondido:** Grafana hospedado em servidor interno, alertas chegam por Telegram e e-mail.

**Pendente:** o que os dashboards mostram? Quais métricas? Tem uptime, tem uso de disco, tem tráfego, tem taxa de erro? Isso vira material de post.

---

## BLOCO 2 — material bruto para o portfólio (3 perguntas)

### 8. Tem alguma coisa sua que eu possa mostrar?

Qualquer uma:

- script que você escreveu e ainda usa
- arquivo de schedule (pode ser sanitizado, sem dado sensível)
- diagrama ou foto da topologia da rede
- print de dashboard, com dado fictício ou mascarado
- saída de log real, com o que for sensível removido
- o `m5copy` documentado, com explicação das flags

Vale para virar repositório, imagem de post, ou slide de entrevista.

### 9. Se você escrevesse um post sobre "o que muda quando o pipeline roda em Debian de verdade em vez de container", qual detalhe te surpreendeu?

A maioria dos candidatos nunca administrou máquina real e não sabe o que não sabe. Sua surprise é conteúdo.

Pensa em coisas como: permissão de arquivo, espaço em disco, diferença entre rodar e testar, o que acontece quando o processo morre no meio, dependência do sistema operacional, atualização de biblioteca quebrando o script.

### 10. Tem algum comando ou conceito de Linux que você descobriu na prática e o curso não ensina?

Ouro para post. Coisas do tipo: a diferença entre `>` e `>>`, encoding de arquivo, um `grep` com expressão regular que resolveu um problema real, `ps aux` e `kill`, permissões, `find` com filtro por data.

---

## BLOCO 3 — para eu montar a skill (2 perguntas)

### 11. Quando você fala "Linux", o que eu devo assumir que você sabe?

**Já sei:** Debian em 4+ máquinas, SSH e MobaXterm, servidor na própria rede, `vim`/`nano`, `awk`/`sed`, `fetch`, Grafana, alertas Telegram e e-mail, Field System, Python.

**Preciso que você complete:**

- Quando eu for falar de Linux contigo, o que posso assumir sem explicar?
- O que eu **não** devo assumir? (ex: posso assumir que sabe `chmod`? e container? e rede?)
- Existe algum tema de Linux que você não manja e prefere que eu não toque?

### 12. Documentação e scripts: escrevo para rodar no seu Debian ou para ser portável?

Três opções:

- **a)** Para o seu servidor Debian, com os comandos que você usa de verdade. Mais rápido de ler, mais honesto.
- **b)** Portável, para rodar em qualquer Linux. Mais útil para portfólio e para GitHub.
- **c)** Os dois: script portátil, README explicando como rodar na sua máquina.

---

## O QUE FAZER COM AS RESPOSTAS

Quando eu ler o arquivo preenchido, o que eu produzo:

1. **Atualizo `CONTEXTO_LINUX_INFRA.md`** com o que for confirmado.
2. **Escrevo as respostas de entrevista** em linguagem que você consiga falar em voz alta, com o porquê de cada escolha.
3. **Escolho 1 ou 2 posts** LinkedIn, baseados no que tiver mais substance.
4. **Monto a skill** de Linux-para-dados, com o que você quer que eu assuma.
5. Se aparecer algo que vale para o currículo, eu sugiro a linha exata. **Você decide e a gente edita.**

Nada vai para o LinkedIn, currículo ou repositório sem você ver e aprovar antes.

---

## STATUS

| Bloco | Situação |
|---|---|
| 1.1 máquinas | respondido |
| 1.2 dia tipo | respondido |
| 1.3 incidente | **pendente, é a prioridade** |
| 1.4 deploy | respondido (não faz), falta confirmar se sobe algo no ar |
| 1.5 armazenamento | respondido (sem container), falta banco e backup |
| 1.6 shell | respondido, falta detalhe |
| 1.7 monitoramento | respondido, falta o que os dashboards mostram |
| 2.8 material | pendente |
| 2.9 surpresa | pendente |
| 2.10 descoberta | pendente |
| 3.11 skill | pendente |
| 3.12 portabilidade | pendente |