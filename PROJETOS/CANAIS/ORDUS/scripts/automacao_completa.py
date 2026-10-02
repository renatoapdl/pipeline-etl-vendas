import json
import os
import subprocess
import sys
from datetime import datetime

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("[VERIFICANDO] Dependencias...")
    
    # Verificar Python
    try:
        print(f"   [OK] Python {sys.version}")
    except:
        print("   [ERRO] Python nao encontrado")
        return False
    
    # Verificar requests
    try:
        import requests
        print("   [OK] requests instalado")
    except:
        print("   [INFO] requests nao encontrado - instalando...")
        subprocess.run(["pip", "install", "requests"])
    
    # Verificar pastas
    pastas = ["content", "audio", "images", "templates"]
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        print(f"   [OK] Pasta {pasta}/ criada/verificada")
    
    return True

def gerar_conteudo():
    """Gera conteúdo da semana"""
    print("\n[CONTEUDO] Gerando conteudo da semana...")
    subprocess.run(["python", "scripts/gerar_conteudo.py"])

def gerar_audios():
    """Gera áudios para todos os posts"""
    print("\n[AUDIO] Gerando audios...")
    subprocess.run(["python", "scripts/gerar_audio.py"])

def criar_templates():
    """Cria templates de texto para cada formato"""
    print("\n[TEMPLATES] Criando templates...")
    
    templates = {
        "reel_manha.txt": """
=== TEMPLATE REEL MANHÃ (60 segundos) ===

Slide 1 (5s):
- Fundo: Azul escuro com estrelas
- Texto: "Bom dia, filho(a) de Deus"
- Fonte: Serifada, dourada

Slide 2 (10s):
- Fundo: Sol nascendo
- Texto: [VERSÍCULO DO DIA]
- Fonte: Serifada, branca

Slide 3 (15s):
- Fundo: Suave, claro
- Texto: [ORAÇÃO DA MANHÃ]
- Fonte: Serifada, escura

Slide 4 (15s):
- Fundo: Cruz + luz
- Texto: [REFLEXÃO]
- Fonte: Sans-serif, escura

Slide 5 (10s):
- Fundo: Branco
- Texto: [ORAÇÃO CONCLUSIVA]
- Fonte: Serifada, escura

Slide 6 (5s):
- Fundo: Logo do canal
- Texto: "Salve e compartilhe"
- Fonte: Sans-serif, branca

=== MÚSICA DE FUNDO ===
- Suave, instrumental
- Volume baixo (20-30%)
- Estilo: Piano ou violão
""",

        "carrossel.txt": """
=== TEMPLATE CARROSSEL (7 slides) ===

Slide 1 (Capa):
- Fundo: Roxo/azul + ícone de pomba
- Texto: "Santo do Dia: [NOME]"
- Data: [DATA]

Slide 2:
- Fundo: Ícone do santo
- Texto: [BREVE BIOGRAFIA]

Slide 3:
- Fundo: Livro aberto
- Texto: [LEITURA DO DIA]

Slide 4:
- Fundo: Salmo
- Texto: [SALMO RESPONSORIAL]

Slide 5:
- Fundo: Mente/lâmpada
- Texto: [REFLEXÃO - 3 PONTOS]

Slide 6:
- Fundo: Mãos orando
- Texto: [ORAÇÃO INTERCESSORA]

Slide 7:
- Fundo: Logo + versículo
- Texto: [VERSÍCULO FINAL]
- CTA: "Compartilhe"

=== FONTES ===
- Títulos: Serifada, branca
- Corpo: Sans-serif, escura
- Versículos: Itálica, dourada
""",

        "reel_noite.txt": """
=== TEMPLATE REEL NOITE (60 segundos) ===

Slide 1 (5s):
- Fundo: Escuro com lua e estrelas
- Texto: "Hora de descansar, filho(a) de Deus"
- Fonte: Serifada, prateada

Slide 2 (10s):
- Fundo: Jesús curando
- Texto: [EVANGELHO DO DIA]
- Fonte: Serifada, branca

Slide 3 (15s):
- Fundo: Noturno, suave
- Texto: [ORAÇÃO DE COMPLETAS]
- Fonte: Serifada, branca

Slide 4 (15s):
- Fundo: Coração em paz
- Texto: [REFLEXÃO]
- Fonte: Sans-serif, branca

Slide 5 (10s):
- Fundo: Azul escuro + estrelas
- Texto: [SALMO DA NOITE]
- Fonte: Serifada, dourada

Slide 6 (5s):
- Fundo: Logo + bênção
- Texto: "A bênção de Deus..."
- Fonte: Serifada, branca

=== MÚSICA DE FUNDO ===
- Calmante, noturna
- Volume baixo (20-30%)
- Estilo: Cordas suaves
"""
    }
    
    for nome, conteudo in templates.items():
        filename = f"templates/{nome}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"   [OK] Template criado: {filename}")

def criar_readme():
    """Cria README com instruções"""
    print("\n[README] Criando README...")
    
    readme = """
# 🙏 Canal Dark Devocionais - Instagram & YouTube

## 📋 Visão Geral
Sistema automatizado para criação e publicação de conteúdo devocional em canais anônimos (dark) no Instagram e YouTube.

## 🗂️ Estrutura de Pastas

```
ORDUS/
├── content/
│   ├── planilha_conteudo.csv      ← Dados dos posts
│   └── textos_semana.json         ← Textos formatados
├── scripts/
│   ├── gerar_conteudo.py          ← Gera conteúdo da semana
│   ├── gerar_audio.py             ← Gera áudios TTS
│   └── automacao_completa.py      ← Script principal
├── templates/
│   ├── reel_manha.txt             ← Template Reel Manhã
│   ├── carrossel.txt              ← Template Carrossel
│   └── reel_noite.txt             ← Template Reel Noite
├── audio/                         ← Áudios MP3 gerados
├── images/                        ← Imagens PNG geradas
└── README.md                      ← Este arquivo
```

## 🚀 Como Usar

### 1. Gerar Conteúdo da Semana
```bash
python scripts/gerar_conteudo.py
```
Isso gera:
- `content/planilha_conteudo.csv`
- `content/textos_semana.json`

### 2. Gerar Áudios
```bash
python scripts/gerar_audio.py
```
Isso gera áudios MP3 na pasta `audio/`

### 3. Criar Imagens no Canva
1. Acesse canva.com
2. Crie 3 templates (Reel Manhã, Carrossel, Reel Noite)
3. Use "Bulk Create" para importar o CSV
4. Gere todas as imagens de uma vez

### 4. Montar Vídeos no CapCut
1. Abra o CapCut
2. Use os templates de texto como guia
3. Adicione imagem + áudio para cada post
4. Exporte os MP4

### 5. Agendar Publicações
**Instagram:**
1. Acesse business.facebook.com
2. Conecte sua conta do Instagram
3. Crie conteúdo → Agendar
4. Escolha data/horário (7h, 12h, 20h)

**YouTube:**
1. Acesse studio.youtube.com
2. Faça upload do vídeo
3. Visibilidade → Agendar
4. Defina data/horário

## 📅 Cronograma Diário

| Horário | Tipo | Formato | Plataforma |
|---------|------|---------|------------|
| 7h | Oração da Manhã | Reel 60s | Instagram + YouTube |
| 12h | Santo do Dia | Carrossel 7 slides | Instagram |
| 20h | Completas | Reel 60s | Instagram + YouTube |

## 🎨 Ferramentas Necessárias

### Gratuitas
- **Canva** - Criação de imagens (Bulk Create)
- **CapCut** - Edição de vídeo
- **Meta Business Suite** - Agendamento Instagram
- **YouTube Studio** - Agendamento YouTube
- **Voicely/SpeechGen** - Geração de áudio TTS

### Opcionais (Automação)
- **Python 3.11+** - Scripts de automação
- **Google Sheets** - Gerenciamento de conteúdo
- **pyCapCut** - Automação do CapCut

## 📝 Personalização

### Alterar Horários
Edite `scripts/gerar_conteudo.py`:
```python
HORARIOS = {
    "manha": "7h",
    "meio_dia": "12h",
    "noite": "20h"
}
```

### Alterar Vozes TTS
Edite `scripts/gerar_audio.py`:
```python
VOZES = {
    "manha": {"voice_id": "pt-BR-Female-1"},
    "meio_dia": {"voice_id": "pt-BR-Male-1"},
    "noite": {"voice_id": "pt-BR-Male-2"}
}
```

### Adicionar Mais Dias
Edite o calendário em `scripts/gerar_conteudo.py`:
```python
CALENDARIO = {
    "07/09": {...},
    "08/09": {...},
    # Adicione mais dias
}
```

## 🎯 Dicas de Sucesso

1. **Consistência**: Poste todos os dias nos mesmos horários
2. **Qualidade**: Prefira qualidade a quantidade
3. **Engajamento**: Responda comentários (pode ser anônimo)
4. **Hashtags**: Use 5-10 hashtags relevantes
5. **Horários**: Teste horários diferentes e veja o que funciona

## 📊 Métricas para Acompanhar

- **Alcance**: Quantas pessoas viram seu conteúdo
- **Engajamento**: Curtidas, comentários, salvamentos
- **Crescimento**: Novos seguidores por semana
- **Cliques**: Links no bio, DMs recebidos

## ⚠️ Avisos Legais

- Todo conteúdo é baseado em domínio público
- Orações do Livro de Oração Comum (domínio público)
- Leituras bíblicas (versões autorizadas)
- Santos e festividades litúrgicas

## 🤝 Contribuindo

Para melhorar o sistema:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit suas alterações
4. Envie um Pull Request

## 📞 Suporte

Em caso de problemas:
- Abra uma issue no GitHub
- Consulte a documentação
- Verifique os logs de erro

---

**Feito com fé e dedicação** ✝️
"""
    
    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    print("   [OK] README.md criado")

def main():
    """Fluxo principal de automação"""
    print("[INICIO] INICIANDO AUTOMACAO COMPLETA")
    print("=" * 50)
    
    # 1. Verificar dependências
    if not verificar_dependencias():
        print("[ERRO] Erro nas dependencias. Abortando.")
        return
    
    # 2. Gerar conteúdo
    gerar_conteudo()
    
    # 3. Gerar áudios
    gerar_audios()
    
    # 4. Criar templates
    criar_templates()
    
    # 5. Criar README
    criar_readme()
    
    print("\n" + "=" * 50)
    print("[SUCESSO] AUTOMACAO CONCLUIDA COM SUCESSO!")
    print("\n[ARQUIVOS] Arquivos criados:")
    print("   - content/planilha_conteudo.csv")
    print("   - content/textos_semana.json")
    print("   - templates/reel_manha.txt")
    print("   - templates/carrossel.txt")
    print("   - templates/reel_noite.txt")
    print("   - README.md")
    print("\n[PROXIMO] Proximo passo: Gerar audios")
    print("   Execute: python scripts/gerar_audio.py")
    print("\n[DEPOIS] Depois: Criar imagens no Canva")
    print("   Use o CSV importado no Bulk Create")

if __name__ == "__main__":
    main()
