# 🚀 Guia de Deploy - YouTube Video Transcriber API

Este guia mostra como fazer deploy da API na Vercel ou Render.

## 📋 Pré-requisitos

1. **Conta na Vercel** (recomendado) ou **Render**
2. **Chave da API OpenAI** - [Obter aqui](https://platform.openai.com/api-keys)
3. **Git configurado** (já feito ✅)

## 🌐 Deploy na Vercel (Recomendado)

### Opção 1: Deploy Automático

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Executar script de deploy
python deploy_vercel.py
```

### Opção 2: Deploy Manual

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Fazer login
vercel login

# 3. Deploy
vercel --prod
```

### Opção 3: Deploy via GitHub

1. **Criar repositório no GitHub:**
   ```bash
   # Adicionar remote
   git remote add origin https://github.com/seu-usuario/youtube-transcriber-api.git
   
   # Push inicial
   git push -u origin master
   ```

2. **Conectar na Vercel:**
   - Acesse [vercel.com](https://vercel.com)
   - Clique em "New Project"
   - Conecte seu repositório GitHub
   - Configure variáveis de ambiente

## ⚙️ Configuração de Variáveis de Ambiente

### Na Vercel Dashboard:
1. Vá para **Settings > Environment Variables**
2. Adicione:
   - `OPENAI_API_KEY` = sua_chave_da_api_openai

### No arquivo .env (local):
```env
OPENAI_API_KEY=sua_chave_da_api_openai
WHISPER_MODEL_SIZE=base
LANGUAGE=pt
```

## 🧪 Testar o Deploy

### 1. Health Check
```bash
curl https://seu-projeto.vercel.app/health
```

### 2. Testar API
```bash
python test_api.py
```

### 3. Usar Cliente Python
```python
from api_client import YouTubeTranscriberClient

client = YouTubeTranscriberClient("https://seu-projeto.vercel.app")
result = client.transcribe_video("https://www.youtube.com/watch?v=VIDEO_ID")

if result["success"]:
    print("Resumo:", result["summary"])
```

## 🔧 Deploy na Render (Alternativa)

### 1. Criar render.yaml
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

## 📊 Monitoramento

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

## 🐛 Troubleshooting

### Erro: "Chave da API OpenAI não configurada"
- Verifique se a variável `OPENAI_API_KEY` está configurada
- Teste localmente primeiro

### Erro: "Timeout"
- Use modelo Whisper menor (`tiny` ou `base`)
- Implemente processamento assíncrono para vídeos longos

### Erro: "FFmpeg não encontrado"
- A Vercel não suporta FFmpeg nativamente
- Use apenas transcrição do YouTube (mais rápido)

## 📈 Limitações

### Vercel
- **Hobby Plan**: 10 segundos por requisição
- **Pro Plan**: 60 segundos por requisição

### Recomendações
1. **Vídeos curtos**: Use endpoint `/transcribe` normal
2. **Vídeos longos**: Use endpoint `/transcribe-async`
3. **Otimização**: Configure `whisper_model_size="tiny"` para processamento mais rápido

## 🎯 URLs da API

Após o deploy, você terá:
- **API**: `https://seu-projeto.vercel.app`
- **Documentação**: `https://seu-projeto.vercel.app/docs`
- **Health Check**: `https://seu-projeto.vercel.app/health`

## 📞 Suporte

Para problemas:
1. Verifique os logs da Vercel
2. Teste localmente com `python main.py`
3. Verifique configuração das variáveis de ambiente

---

**Deploy realizado com ❤️ por Bruno**
