import json
import os
import sys
import asyncio

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tentar importar edge-tts
try:
    import edge_tts
    EDGE_TTS_DISPONIVEL = True
except ImportError:
    EDGE_TTS_DISPONIVEL = False
    print("[INFO] edge-tts nao encontrado. Instalando...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts
    EDGE_TTS_DISPONIVEL = True

# Vozes disponíveis (Microsoft Edge Neural)
VOZES = {
    "manha": {
        "nome": "Francisca (Feminina Suave)",
        "voice_id": "pt-BR-FranciscaNeural",
        "rate": "-10%",
        "pitch": "+0Hz"
    },
    "meio_dia": {
        "nome": "Antonio (Masculina Formal)",
        "voice_id": "pt-BR-AntonioNeural",
        "rate": "+0%",
        "pitch": "+0Hz"
    },
    "noite": {
        "nome": "Thalita (Feminina Calmante)",
        "voice_id": "pt-BR-ThalitaNeural",
        "rate": "-15%",
        "pitch": "-5Hz"
    }
}

async def gerar_audio_edge_tts(texto, voice_id, rate, pitch, output_file):
    """Gera áudio usando Edge TTS (Microsoft Neural) - GRATUITO"""
    try:
        communicate = edge_tts.Communicate(
            text=texto,
            voice=voice_id,
            rate=rate,
            pitch=pitch
        )
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"[ERRO] Edge TTS: {e}")
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
        
        # Usar Edge TTS para gerar áudio
        sucesso = asyncio.run(gerar_audio_edge_tts(
            post['texto'],
            voz['voice_id'],
            voz['rate'],
            voz['pitch'],
            filename
        ))
        
        if sucesso:
            print(f"   [OK] Audio gerado: {filename}")
            posts_processados += 1
        else:
            print(f"   [ERRO] Falha ao gerar audio")
    
    return posts_processados

if __name__ == "__main__":
    print("[INICIO] Iniciando geracao de audios com Edge TTS...")
    print("[INFO] Edge TTS usa vozes neurais da Microsoft (gratuitas)")
    print("[INFO] Qualidade: Alta (vozes neurais)")
    print("[INFO] Limite: Sem limite conhecido")
    print("-" * 50)
    
    total = processar_posts("content/textos_semana.json")
    
    print("-" * 50)
    print(f"[SUCESSO] {total} audios gerados com sucesso!")
    print(f"[LOCAL] Arquivos salvos na pasta: audio/")
