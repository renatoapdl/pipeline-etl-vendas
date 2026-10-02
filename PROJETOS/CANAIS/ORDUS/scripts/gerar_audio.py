import requests
import json
import os
import sys
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurações
VOICELY_URL = "https://tryvoicely.com/api/generate"
SPEECHGEN_URL = "https://speechgen.io/api/generate"

# Vozes disponíveis
VOZES = {
    "manha": {
        "nome": "Feminina Brasileira",
        "voice_id": "pt-BR-Female-1",
        "descricao": "Voz suave para a oração da manhã"
    },
    "meio_dia": {
        "nome": "Neutra Brasileira",
        "voice_id": "pt-BR-Male-1",
        "descricao": "Voz clara para a reflexão do meio-dia"
    },
    "noite": {
        "nome": "Masculina Brasileira",
        "voice_id": "pt-BR-Male-2",
        "descricao": "Voz grave e calmante para a noite"
    }
}

def gerar_audio_voicely(texto, voice_id, output_file):
    """Gera áudio usando Voicely (grátis)"""
    try:
        response = requests.post(VOICELY_URL, json={
            "text": texto,
            "voice": voice_id,
            "speed": 1.0
        })
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"[ERRO] Voicely: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERRO] Voicely: {e}")
        return False

def gerar_audio_speechgen(texto, voice_id, output_file):
    """Gera áudio usando SpeechGen.io (alternativa)"""
    try:
        response = requests.post(SPEECHGEN_URL, json={
            "text": texto,
            "voice": voice_id,
            "format": "mp3"
        })
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"[ERRO] SpeechGen: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERRO] SpeechGen: {e}")
        return False

def processar_posts(posts_file):
    """Processa todos os posts e gera áudios"""
    # Carregar posts
    with open(posts_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    # Criar pasta de áudio
    os.makedirs("audio", exist_ok=True)
    
    # Processar cada post
    for post in posts:
        tipo = post['tipo']
        data = post['data'].replace('/', '_')
        
        # Determinar voz baseado no tipo
        if 'Manha' in tipo:
            voz = VOZES['manha']
        elif 'Noite' in tipo:
            voz = VOZES['noite']
        else:
            voz = VOZES['meio_dia']
        
        # Nome do arquivo
        filename = f"audio/{data}_{tipo}.mp3"
        
        print(f"[AUDIO] Gerando audio: {filename}")
        print(f"   Voz: {voz['nome']}")
        
        # Tentar Voicely primeiro, depois SpeechGen
        sucesso = gerar_audio_voicely(post['texto'], voz['voice_id'], filename)
        
        if not sucesso:
            print("   Tentando SpeechGen...")
            sucesso = gerar_audio_speechgen(post['texto'], voz['voice_id'], filename)
        
        if sucesso:
            print(f"   [OK] Audio gerado: {filename}")
        else:
            print(f"   [ERRO] Falha ao gerar audio")

if __name__ == "__main__":
    print("[INICIO] Iniciando geracao de audios...")
    processar_posts("content/textos_semana.json")
    print("[SUCESSO] Geracao de audios concluida!")
