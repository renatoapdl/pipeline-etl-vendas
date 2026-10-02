import json
import os
import sys

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tentar importar gTTS
try:
    from gtts import gTTS
    GTTS_DISPONIVEL = True
except ImportError:
    GTTS_DISPONIVEL = False
    print("[INFO] gTTS nao encontrado. Instalando...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "gTTS"])
    from gtts import gTTS
    GTTS_DISPONIVEL = True

def gerar_audio_gtts(texto, lang, output_file):
    """Gera áudio usando gTTS (Google Text-to-Speech) - GRATUITO"""
    try:
        # gTTS usa a API do Google Translate (gratuita)
        tts = gTTS(text=texto, lang=lang, slow=False)
        tts.save(output_file)
        return True
    except Exception as e:
        print(f"[ERRO] gTTS: {e}")
        return False

def processar_posts(posts_file):
    """Processa todos os posts e gera áudios"""
    # Carregar posts
    with open(posts_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    # Criar pasta de áudio
    os.makedirs("audio", exist_ok=True)
    
    # Processar cada post
    posts_processados = 0
    for post in posts:
        tipo = post['tipo']
        data = post['data'].replace('/', '_')
        
        # Determinar idioma (português do Brasil)
        lang = 'pt-br'
        
        # Nome do arquivo
        filename = f"audio/{data}_{tipo}.mp3"
        
        print(f"[AUDIO] Gerando audio: {filename}")
        
        # Usar gTTS para gerar áudio
        sucesso = gerar_audio_gtts(post['texto'], lang, filename)
        
        if sucesso:
            print(f"   [OK] Audio gerado: {filename}")
            posts_processados += 1
        else:
            print(f"   [ERRO] Falha ao gerar audio")
    
    return posts_processados

if __name__ == "__main__":
    print("[INICIO] Iniciando geracao de audios com gTTS...")
    print("[INFO] gTTS usa a API gratuita do Google Translate")
    print("[INFO] Qualidade: Boa para narracao")
    print("[INFO] Limite: Sem limite conhecido")
    print("-" * 50)
    
    total = processar_posts("content/textos_semana.json")
    
    print("-" * 50)
    print(f"[SUCESSO] {total} audios gerados com sucesso!")
    print(f"[LOCAL] Arquivos salvos na pasta: audio/")
