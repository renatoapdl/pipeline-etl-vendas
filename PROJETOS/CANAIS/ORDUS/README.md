
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
│   ├── GUIA_CANVA.md              ← Especificações detalhadas de cores/fontes
│   ├── GUIA_PASSO_A_PASSO.md      ← Guia completo para criar no Canva
│   ├── mockup_reel_manha.html     ← Mockup visual Reel Manhã
│   ├── mockup_reel_noite.html     ← Mockup visual Reel Noite
│   ├── mockup_carrossel.html      ← Mockup visual Carrossel
│   ├── reel_manha.txt             ← Template Reel Manhã (texto)
│   ├── carrossel.txt              ← Template Carrossel (texto)
│   └── reel_noite.txt             ← Template Reel Noite (texto)
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
Isso gera áudios MP3 com vozes neurais da Microsoft na pasta `audio/`

**Alternativas:**
- `python scripts/gerar_audio_gtts.py` - Usa gTTS (qualidade básica)
- `python scripts/gerar_audio.py` - Usa APIs externas (pode falhar)

### 3. Criar Imagens no Canva
1. Acesse canva.com
2. Consulte os guias em `templates/`:
   - `GUIA_CANVA.md` - Especificações de cores, fontes e layout
   - `GUIA_PASSO_A_PASSO.md` - Passo a passo detalhado
   - `mockup_*.html` - Mockups visuais para referência
3. Crie 3 templates:
   - Reel Manhã (1080x1920 px)
   - Carrossel (1080x1080 px)
   - Reel Noite (1080x1920 px)
4. Use "Bulk Create" para importar o CSV
5. Gere todas as imagens de uma vez

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
Edite `scripts/gerar_audio_edge.py`:
```python
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
```

**Vozes disponíveis (Edge TTS):**
- `pt-BR-FranciscaNeural` - Feminina, suave
- `pt-BR-AntonioNeural` - Masculina, formal
- `pt-BR-ThalitaNeural` - Feminina, jovem e amigável
- `pt-BR-JulioNeural` - Masculina, casual
- `pt-BR-LeilaNeural` - Feminina, madura
- `pt-BR-NicolauNeural` - Masculina, profunda
- `pt-BR-ValeriaNeural` - Feminina, profissional
- `pt-BR-YaraNeural` - Feminina, expressiva

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
