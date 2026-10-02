# 🙏 Canal Dark Devocionais - Instagram & YouTube

## 📋 Visão Geral
Sistema automatizado para criação e publicação de conteúdo devocional em canais anônimos (dark) no Instagram e YouTube.

## 🗂️ Estrutura de Pastas

```
ORDUS/
├── content/
│   ├── planilha_conteudo.csv      ← Dados dos posts (21 posts)
│   └── textos_semana.json         ← Textos formatados
├── scripts/
│   ├── gerar_conteudo.py          ← Gera conteúdo da semana
│   ├── gerar_audio.py             ← Gera áudios TTS (alternativo)
│   ├── gerar_audio_gtts.py        ← Gera áudios com gTTS
│   ├── gerar_audio_edge.py        ← Gera áudios com Edge TTS (RECOMENDADO)
│   └── automacao_completa.py      ← Script principal
├── templates/
│   ├── reel_manha.txt             ← Template Reel Manhã
│   ├── carrossel.txt              ← Template Carrossel
│   └── reel_noite.txt             ← Template Reel Noite
├── audio/                         ← 21 áudios MP3 gerados
├── images/                        ← Imagens PNG (a criar no Canva)
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

### 2. Gerar Áudios (RECOMENDADO: Edge TTS)
```bash
python scripts/gerar_audio_edge.py
```
✅ **21 áudios MP3 já gerados na pasta `audio/` com vozes neurais da Microsoft**

**Alternativas:**
- `python scripts/gerar_audio_gtts.py` - Usa gTTS (qualidade básica)
- `python scripts/gerar_audio.py` - Usa APIs externas (pode falhar)

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
- **Edge TTS** - Geração de áudio com vozes neurais (RECOMENDADO)
- **gTTS** - Geração de áudio alternativa

### Opcionais (Automação)
- **Python 3.11+** - Scripts de automação
- **Google Sheets** - Gerenciamento de conteúdo
- **pyCapCut** - Automação do CapCut

## 📊 Arquivos Gerados

### Conteúdo (7 dias × 3 posts = 21 posts)
- `content/planilha_conteudo.csv` - 13 KB
- `content/textos_semana.json` - 17 KB

### Áudios (21 arquivos MP3)
- `audio/07_09_2026_Reel_Manha.mp3` - 200 KB
- `audio/07_09_2026_Carrossel.mp3` - 470 KB
- `audio/07_09_2026_Reel_Noite.mp3` - 360 KB
- `audio/08_09_2026_Reel_Manha.mp3` - 190 KB
- `audio/08_09_2026_Carrossel.mp3` - 459 KB
- `audio/08_09_2026_Reel_Noite.mp3` - 369 KB
- `audio/09_09_2026_Reel_Manha.mp3` - 195 KB
- `audio/09_09_2026_Carrossel.mp3` - 456 KB
- `audio/09_09_2026_Reel_Noite.mp3` - 354 KB
- `audio/10_09_2026_Reel_Manha.mp3` - 195 KB
- `audio/10_09_2026_Carrossel.mp3` - 467 KB
- `audio/10_09_2026_Reel_Noite.mp3` - 367 KB
- `audio/11_09_2026_Reel_Manha.mp3` - 195 KB
- `audio/11_09_2026_Carrossel.mp3` - 474 KB
- `audio/11_09_2026_Reel_Noite.mp3` - 360 KB
- `audio/12_09_2026_Reel_Manha.mp3` - 195 KB
- `audio/12_09_2026_Carrossel.mp3` - 461 KB
- `audio/12_09_2026_Reel_Noite.mp3` - 361 KB
- `audio/13_09_2026_Reel_Manha.mp3` - 195 KB
- `audio/13_09_2026_Carrossel.mp3` - 463 KB
- `audio/13_09_2026_Reel_Noite.mp3` - 362 KB

### Templates
- `templates/reel_manha.txt` - 751 bytes
- `templates/carrossel.txt` - 675 bytes
- `templates/reel_noite.txt` - 785 bytes

### Scripts
- `scripts/gerar_conteudo.py` - 6.4 KB
- `scripts/gerar_audio.py` - 3.5 KB
- `scripts/gerar_audio_gtts.py` - 2.3 KB
- `scripts/gerar_audio_edge.py` - 2.5 KB
- `scripts/automacao_completa.py` - 9.6 KB

## 📅 Calendário Litúrgico (07-13 de Setembro 2026)

| Data | Santo | Evangelho | Tema |
|------|-------|-----------|------|
| 07/09 | Nossa Senhora da Vitória | Lc 4,31-37 | A autoridade de Jesus |
| 08/09 | Natividade de Nossa Senhora | Mt 1,1-16.18-23 | A origem de Maria |
| 09/09 | São Pedro Clérigo | Lc 6,12-19 | Unidos em Cristo |
| 10/09 | São Nicolau de Tolentino | Mt 24,42-51 | Vigilância e preparação |
| 11/09 | São João Gabriel de Boyne | Lc 6,27-36 | Amor aos inimigos |
| 12/09 | Santos Nomes de Maria | Lc 6,39-42 | Humildade e julgamento |
| 13/09 | São João Crisóstomo | Lc 6,43-49 | Bons frutos e sabedoria |

## 🎯 Próximos Passos

1. **Criar templates no Canva** (Reel Manhã, Carrossel, Reel Noite)
2. **Importar CSV no Bulk Create** do Canva
3. **Gerar imagens** para cada post
4. **Montar vídeos no CapCut** (imagem + áudio)
5. **Agendar publicações** no Meta Business Suite e YouTube Studio

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

---

**Sistema criado com sucesso!** ✝️
**Total de arquivos:** 29
**Total de áudios:** 21 MP3 (vozes neurais Edge TTS)
**Total de posts:** 21 (7 dias × 3 posts)
**Qualidade dos áudios:** Alta (vozes neurais Microsoft)
