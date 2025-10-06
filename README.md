# 🎬 YouTube Video Transcriber & Summarizer

Sistema simplificado para transcrever e resumir vídeos do YouTube usando OpenAI.

## ✨ Características

- **Transcrição Inteligente**: YouTube Transcript API + Whisper local
- **Resumos de Alta Qualidade**: OpenAI GPT-3.5-turbo
- **Fácil de Usar**: Interface simples e intuitiva
- **Otimizado para Deploy**: Versão limpa e eficiente

## 🚀 Instalação Rápida

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd youtube-transcriber
```

### 2. Execute o script de deploy
```bash
python deploy.py
```

### 3. Configure sua chave da API OpenAI
Edite o arquivo `.env` e adicione sua chave:
```
OPENAI_API_KEY=sua_chave_aqui
```

## 📖 Como Usar

### Uso Básico
```bash
python app.py
```

### Uso Programático
```python
from youtube_transcriber import YouTubeTranscriber

# Inicializar
transcriber = YouTubeTranscriber(
    openai_api_key="sua_chave_aqui",
    whisper_model_size="base"
)

# Processar vídeo
results = transcriber.process_video("https://www.youtube.com/watch?v=VIDEO_ID")

if results["success"]:
    print("Transcrição:", results["transcript"])
    print("Resumo:", results["summary"])
```

## ⚙️ Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` com:
```
OPENAI_API_KEY=sua_chave_aqui
WHISPER_MODEL_SIZE=base
LANGUAGE=pt
```

### Modelos Whisper Disponíveis
- `tiny`: Mais rápido, menor qualidade
- `base`: Equilíbrio (recomendado)
- `small`: Boa qualidade
- `medium`: Alta qualidade
- `large`: Melhor qualidade, mais lento

## 📁 Estrutura do Projeto

```
youtube-transcriber/
├── youtube_transcriber.py    # Classe principal
├── app.py                   # Aplicação principal
├── deploy.py                # Script de deploy
├── requirements.txt         # Dependências
├── config.env.example      # Exemplo de configuração
├── README.md               # Este arquivo
└── ffmpeg.exe             # FFmpeg (incluído)
```

## 🔧 Dependências

- `yt-dlp`: Download de vídeos
- `youtube-transcript-api`: Transcrição direta
- `openai`: API do OpenAI
- `openai-whisper`: Transcrição local
- `requests`: Requisições HTTP

## 🎯 Funcionalidades

### 1. Transcrição
- **YouTube Transcript API**: Instantâneo (se disponível)
- **Whisper Local**: Fallback para qualquer vídeo

### 2. Resumo
- **OpenAI GPT-3.5-turbo**: Resumos inteligentes e contextuais

### 3. Processamento
- **Download automático**: Se necessário
- **Extração de áudio**: Via FFmpeg
- **Limpeza automática**: Arquivos temporários

## 🚀 Deploy

### Deploy Local
```bash
python deploy.py
python app.py
```

### Deploy em Servidor
1. Instale as dependências
2. Configure as variáveis de ambiente
3. Execute `python app.py`

## 📊 Performance

### Tempos Estimados (vídeo de 10 minutos)
- YouTube Transcript: ~5 segundos
- Whisper (base): ~2-3 minutos
- OpenAI Resumo: ~10-15 segundos

### Requisitos de Sistema
- **Python**: 3.8+
- **RAM**: 4GB+ (8GB+ recomendado)
- **Espaço**: ~2GB para modelos Whisper
- **Internet**: Para APIs

## 🐛 Solução de Problemas

### Erro: "Chave da API OpenAI não encontrada"
- Configure a variável de ambiente `OPENAI_API_KEY`
- Ou edite o arquivo `.env`

### Erro: "FFmpeg não encontrado"
- Execute `python deploy.py` para baixar automaticamente
- Ou instale manualmente: https://ffmpeg.org/download.html

### Erro: "URL do YouTube inválida"
- Verifique se a URL está correta
- Use URLs do YouTube válidas

## 📞 Suporte

Se encontrar problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme se a chave da API OpenAI está configurada
3. Verifique se o FFmpeg está disponível

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ por Bruno**