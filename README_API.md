# 🎬 YouTube Video Transcriber API

API FastAPI para transcrever e resumir vídeos do YouTube usando OpenAI.

## 🚀 Deploy na Vercel

### 1. Preparar o Repositório

```bash
# Estrutura do projeto
youtube-transcriber-api/
├── main.py              # API FastAPI
├── youtube_transcriber.py  # Classe principal
├── vercel.json          # Configuração da Vercel
├── requirements.txt     # Dependências
├── api_client.py        # Cliente de exemplo
└── README_API.md        # Esta documentação
```

### 2. Configurar Variáveis de Ambiente

Na Vercel Dashboard:
1. Vá para Settings > Environment Variables
2. Adicione: `OPENAI_API_KEY` = sua chave da API OpenAI

### 3. Deploy

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel

# Ou conectar repositório GitHub na Vercel Dashboard
```

## 📖 Documentação da API

### Base URL
```
https://seu-projeto.vercel.app
```

### Endpoints

#### `GET /`
Informações básicas da API

#### `GET /health`
Health check da API

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API funcionando corretamente",
  "version": "1.0.0"
}
```

#### `POST /transcribe`
Transcreve e resume um vídeo do YouTube

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "whisper_model_size": "base",
  "language": "pt",
  "max_tokens": 500
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "transcript": "Transcrição completa do vídeo...",
  "summary": "Resumo inteligente do vídeo...",
  "method": "youtube_transcript",
  "processing_time": 15.5,
  "error": null
}
```

#### `POST /transcribe-async`
Inicia processamento assíncrono (para vídeos longos)

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "task_id": "uuid-da-tarefa",
  "status": "processing",
  "message": "Vídeo sendo processado em background"
}
```

## 🔧 Uso com Python

### Cliente Simples

```python
import requests

# Transcrever vídeo
response = requests.post(
    "https://seu-projeto.vercel.app/transcribe",
    json={
        "url": "https://www.youtube.com/watch?v=VIDEO_ID"
    }
)

result = response.json()
if result["success"]:
    print("Resumo:", result["summary"])
    print("Transcrição:", result["transcript"])
```

### Cliente Avançado

```python
from api_client import YouTubeTranscriberClient

# Inicializar cliente
client = YouTubeTranscriberClient("https://seu-projeto.vercel.app")

# Transcrever vídeo
result = client.transcribe_video("https://www.youtube.com/watch?v=VIDEO_ID")

if result["success"]:
    print("Resumo:", result["summary"])
```

## 🌐 Uso com JavaScript/Node.js

```javascript
// Transcrever vídeo
const response = await fetch('https://seu-projeto.vercel.app/transcribe', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=VIDEO_ID'
  })
});

const result = await response.json();
if (result.success) {
  console.log('Resumo:', result.summary);
  console.log('Transcrição:', result.transcript);
}
```

## 🌐 Uso com cURL

```bash
# Health check
curl https://seu-projeto.vercel.app/health

# Transcrever vídeo
curl -X POST https://seu-projeto.vercel.app/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }'
```

## 📊 Limitações da Vercel

### Timeout
- **Hobby Plan**: 10 segundos por requisição
- **Pro Plan**: 60 segundos por requisição

### Recomendações
1. **Vídeos curtos**: Use endpoint `/transcribe` normal
2. **Vídeos longos**: Use endpoint `/transcribe-async` (implementar sistema de filas)
3. **Otimização**: Configure `whisper_model_size="tiny"` para processamento mais rápido

## 🔧 Configurações Avançadas

### Modelos Whisper
- `tiny`: Mais rápido, menor qualidade
- `base`: Equilíbrio (recomendado para API)
- `small`: Boa qualidade
- `medium`: Alta qualidade (pode exceder timeout)
- `large`: Melhor qualidade (não recomendado para API)

### Idiomas Suportados
- `pt`: Português
- `en`: Inglês
- `es`: Espanhol
- `fr`: Francês
- E outros códigos ISO 639-1

## 🐛 Troubleshooting

### Erro: "Chave da API OpenAI não configurada"
- Verifique se a variável `OPENAI_API_KEY` está configurada na Vercel

### Erro: "Timeout"
- Use modelo Whisper menor (`tiny` ou `base`)
- Implemente processamento assíncrono para vídeos longos

### Erro: "FFmpeg não encontrado"
- A Vercel não suporta FFmpeg nativamente
- Use apenas transcrição do YouTube (mais rápido)

## 📈 Monitoramento

### Logs da Vercel
```bash
# Ver logs em tempo real
vercel logs

# Ver logs de uma função específica
vercel logs --function=main
```

### Métricas
- Acesse o dashboard da Vercel para ver métricas de uso
- Monitore tempo de resposta e erros

## 🚀 Deploy Alternativo (Render)

Se preferir usar Render:

### 1. Criar `render.yaml`
```yaml
services:
  - type: web
    name: youtube-transcriber-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

### 2. Deploy
1. Conecte repositório GitHub
2. Configure variáveis de ambiente
3. Deploy automático

## 📞 Suporte

Para problemas:
1. Verifique os logs da Vercel
2. Teste localmente com `python main.py`
3. Verifique configuração das variáveis de ambiente

---

**API desenvolvida com ❤️ por Bruno**
