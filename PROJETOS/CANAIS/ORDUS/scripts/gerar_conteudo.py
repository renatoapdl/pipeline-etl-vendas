import csv
import json
import os
import sys
from datetime import datetime, timedelta

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Calendário litúrgico simplificado
CALENDARIO = {
    "07/09": {
        "santo": "Nossa Senhora da Vitória",
        "evangelho": "Lucas capítulo 4, versículos 31 a 37",
        "primeira_leitura": "Primeira Carta de São Paulo aos Coríntios capítulo 2, versículos 10 a 16",
        "salmo": "Salmo cento e quarenta e quatro",
        "salmo_numero": "144",
        "tema": "A autoridade de Jesus"
    },
    "08/09": {
        "santo": "Natividade de Nossa Senhora",
        "evangelho": "Mateus capítulo 1, versículos 1 a 16 e 18 a 23",
        "primeira_leitura": "Miquéias capítulo 5, versículos 2 a 4",
        "salmo": "Salmo treze",
        "salmo_numero": "13",
        "tema": "A origem de Maria"
    },
    "09/09": {
        "santo": "São Pedro Clérigo",
        "evangelho": "Lucas capítulo 6, versículos 12 a 19",
        "primeira_leitura": "Primeira Carta de São Paulo aos Coríntios capítulo 3, versículos 1 a 9",
        "salmo": "Salmo trinta e três",
        "salmo_numero": "33",
        "tema": "Unidos em Cristo"
    },
    "10/09": {
        "santo": "São Nicolau de Tolentino",
        "evangelho": "Mateus capítulo 24, versículos 42 a 51",
        "primeira_leitura": "Primeira Carta de São Paulo aos Coríntios capítulo 3, versículos 10 a 17",
        "salmo": "Salmo vinte e quatro",
        "salmo_numero": "24",
        "tema": "Vigilância e preparação"
    },
    "11/09": {
        "santo": "São João Gabriel de Boyne",
        "evangelho": "Lucas capítulo 6, versículos 27 a 36",
        "primeira_leitura": "Primeira Carta de São Paulo aos Coríntios capítulo 3, versículos 18 a 23",
        "salmo": "Salmo vinte e sete",
        "salmo_numero": "27",
        "tema": "Amor aos inimigos"
    },
    "12/09": {
        "santo": "Santos Nomes de Maria",
        "evangelho": "Lucas capítulo 6, versículos 39 a 42",
        "primeira_leitura": "Primeira Carta de São Paulo aos Coríntios capítulo 4, versículos 1 a 5",
        "salmo": "Salmo cento e trinta",
        "salmo_numero": "130",
        "tema": "Humildade e julgamento"
    },
    "13/09": {
        "santo": "São João Crisóstomo",
        "evangelho": "Lucas capítulo 6, versículos 43 a 49",
        "primeira_leitura": "Primeira Carta de São Paulo aos Coríntios capítulo 4, versículos 6 a 15",
        "salmo": "Salmo cento e treze",
        "salmo_numero": "113",
        "tema": "Bons frutos e sabedoria"
    }
}

def gerar_texto_oracao_manha(salmo):
    return f"""Ó Senhor, abri os nossos lábios.
E a nossa boca anunciará os vossos louvores.

{salmo}.

Deus onipotente, fonte de todo dom perfeito,
semeai em nossos corações o amor ao vosso nome.
Por Jesus Cristo, nosso Senhor. Amém."""

def gerar_texto_carrossel(dados):
    return f"""Santo do Dia. {dados['santo']}.

Leitura do Dia.
{dados['primeira_leitura']}.

{dados['salmo']}.

Reflexão.
Primeiro. O Espírito de Deus penetra tudo.
Segundo. Como os santos foram guiados, também nós somos.
Terceiro. O pensamento de Cristo está disponível a todos.

Oração.
Senhor, concedei-nos o vosso Espírito para compreendermos vossos caminhos. Amém.

Versículo final.
Nós, porém, temos o pensamento de Cristo."""

def gerar_texto_oracao_noite(evangelho):
    return f"""Hora de descansar, filho de Deus.

{evangelho}.

Oração de Completas.
Vindeste, ó Espírito Santo, encher os vossos apóstolos.
Ench também os nossos corações de paz esta noite.

Salmo quatro, verso nove.
Em paz me deitarei e adormecerei, porque só vós, Senhor, me fazestes habitar em segurança.

A bênção de Deus todo-poderoso desça sobre vós esta noite. Amém. Boa noite."""

def gerar_conteudo_semana(data_inicio):
    posts = []
    for i in range(7):
        data = data_inicio + timedelta(days=i)
        data_str = data.strftime("%d/%m")
        
        if data_str in CALENDARIO:
            dados = CALENDARIO[data_str]
            
            # Reel Manhã
            posts.append({
                "data": data.strftime("%d/%m/%Y"),
                "tipo": "Reel_Manha",
                "hora": "7h",
                "titulo": f"Oração do Despertar - {data.strftime('%d/%m')}",
                "texto": gerar_texto_oracao_manha(dados["salmo"]),
                "versiculo": f"{dados['salmo']}",
                "oracao": "Ó Senhor, abri os nossos lábios...",
                "reflexao": f"Hoje a Igreja celebra {dados['santo']}. {dados['tema']}.",
                "hashtags": "#oraçãodamanhã #devocional #fé #paz #livrodeoraçãocomum",
                "legenda": f"{dados['salmo']} - {dados['tema']}. Comece este dia com Deus."
            })
            
            # Carrossel
            posts.append({
                "data": data.strftime("%d/%m/%Y"),
                "tipo": "Carrossel",
                "hora": "12h",
                "titulo": f"Santo do Dia - {dados['santo']}",
                "texto": gerar_texto_carrossel(dados),
                "versiculo": dados["primeira_leitura"],
                "oracao": "Senhor, concedei-nos o vosso Espírito...",
                "reflexao": f"{dados['tema']}. O Espírito de Deus penetra tudo.",
                "hashtags": "#santododia #fé #carrossel #devocional",
                "legenda": f"{data.strftime('%d/%m')} - {dados['santo']}. {dados['tema']}."
            })
            
            # Reel Noite
            posts.append({
                "data": data.strftime("%d/%m/%Y"),
                "tipo": "Reel_Noite",
                "hora": "20h",
                "titulo": f"Completas - {data.strftime('%d/%m')}",
                "texto": gerar_texto_oracao_noite(dados["evangelho"]),
                "versiculo": dados["evangelho"],
                "oracao": "Vindeste, ó Espírito Santo...",
                "reflexao": f"Assim como Jesus ensina com autoridade no evangelho de {dados['evangelho']}.",
                "hashtags": "#oraçãodanoite #completas #fé #paz",
                "legenda": f"{dados['evangelho']} - Jesus ensina com autoridade. Entregue sua paz ao Senhor."
            })
    
    return posts

def salvar_csv(posts, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=posts[0].keys())
        writer.writeheader()
        writer.writerows(posts)

def salvar_json(posts, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Gerar conteúdo para a próxima semana (a partir de 07/09/2026)
    data_inicio = datetime(2026, 9, 7)
    posts = gerar_conteudo_semana(data_inicio)
    
    # Criar pasta content se não existir
    os.makedirs("content", exist_ok=True)
    
    # Salvar arquivos
    salvar_csv(posts, "content/planilha_conteudo.csv")
    salvar_json(posts, "content/textos_semana.json")
    
    print(f"[SUCESSO] {len(posts)} posts gerados com sucesso!")
    print(f"[ARQUIVO] CSV: content/planilha_conteudo.csv")
    print(f"[ARQUIVO] JSON: content/textos_semana.json")
