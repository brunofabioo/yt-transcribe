"""
Script de Deploy para Render.com
===============================

Script para configurar e fazer deploy da API na Render.
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def verificar_arquivos_render():
    """Verifica se todos os arquivos necessários para Render existem"""
    print("🔍 Verificando arquivos para Render...")
    
    arquivos_necessarios = [
        "main.py",
        "youtube_transcriber.py", 
        "requirements.txt",
        "render.yaml"
    ]
    
    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if not Path(arquivo).exists():
            arquivos_faltando.append(arquivo)
    
    if arquivos_faltando:
        print(f"❌ Arquivos faltando: {', '.join(arquivos_faltando)}")
        return False
    
    print("✅ Todos os arquivos necessários encontrados!")
    return True


def verificar_requirements():
    """Verifica se o requirements.txt está otimizado para Render"""
    print("📦 Verificando requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        # Verificar se tem as dependências essenciais
        dependencias_essenciais = [
            "fastapi",
            "uvicorn",
            "yt-dlp",
            "youtube-transcript-api",
            "openai",
            "openai-whisper"
        ]
        
        faltando = []
        for dep in dependencias_essenciais:
            if dep not in content.lower():
                faltando.append(dep)
        
        if faltando:
            print(f"⚠️ Dependências faltando: {', '.join(faltando)}")
            return False
        
        print("✅ requirements.txt está correto!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar requirements.txt: {e}")
        return False


def criar_arquivo_env_exemplo():
    """Cria arquivo .env.example para Render"""
    print("📝 Criando arquivo .env.example...")
    
    env_content = """# YouTube Video Transcriber API - Render.com
# Copie este arquivo para .env e configure suas variáveis

# Chave da API OpenAI (obrigatória)
OPENAI_API_KEY=your_openai_api_key_here

# Configurações opcionais
WHISPER_MODEL_SIZE=base
LANGUAGE=pt

# Render.com configurações
PORT=10000
"""
    
    try:
        with open(".env.example", "w") as f:
            f.write(env_content)
        print("✅ Arquivo .env.example criado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env.example: {e}")
        return False


def testar_api_localmente():
    """Testa se a API funciona localmente"""
    print("🧪 Testando API localmente...")
    
    try:
        # Verificar se as dependências estão instaladas
        import fastapi
        import uvicorn
        print("✅ FastAPI e Uvicorn disponíveis")
        
        # Testar importação da API
        from main import app
        print("✅ API importada com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependências não instaladas: {e}")
        print("Execute: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        return False


def criar_instrucoes_deploy():
    """Cria arquivo com instruções de deploy"""
    print("📋 Criando instruções de deploy...")
    
    instrucoes = """# 🚀 Deploy na Render.com - YouTube Video Transcriber API

## 📋 Pré-requisitos

1. **Conta na Render.com** - [Criar conta](https://render.com)
2. **Chave da API OpenAI** - [Obter aqui](https://platform.openai.com/api-keys)
3. **Repositório no GitHub** - [brunofabioo/yt-transcribe](https://github.com/brunofabioo/yt-transcribe)

## 🔧 Passos para Deploy

### 1. Acesse Render.com
- Vá para [render.com](https://render.com)
- Faça login ou crie uma conta

### 2. Criar Novo Serviço
- Clique em "New +"
- Selecione "Web Service"
- Conecte seu repositório GitHub: `brunofabioo/yt-transcribe`

### 3. Configurar o Serviço
- **Name**: `youtube-transcriber-api`
- **Environment**: `Python 3`
- **Region**: `Oregon (US West)`
- **Branch**: `master`
- **Root Directory**: (deixe vazio)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4. Configurar Variáveis de Ambiente
- **OPENAI_API_KEY**: `sua_chave_da_api_openai`
- **WHISPER_MODEL_SIZE**: `base`
- **LANGUAGE**: `pt`

### 5. Deploy
- Clique em "Create Web Service"
- Aguarde o build e deploy (5-10 minutos)

## 🧪 Testar o Deploy

### Health Check
```bash
curl https://youtube-transcriber-api.onrender.com/health
```

### Testar API
```bash
curl -X POST https://youtube-transcriber-api.onrender.com/transcribe \\
  -H "Content-Type: application/json" \\
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

## 📊 Monitoramento

- **Logs**: Render Dashboard > Seu Serviço > Logs
- **Métricas**: Render Dashboard > Seu Serviço > Metrics
- **Uptime**: Render Dashboard > Seu Serviço > Uptime

## 🔧 Configurações Avançadas

### Plano Gratuito
- **Limitações**: 750 horas/mês, sleep após 15 min de inatividade
- **Recomendação**: Ideal para testes e desenvolvimento

### Plano Pago
- **Vantagens**: Sem sleep, mais recursos, domínio personalizado
- **Recomendação**: Para produção

## 🐛 Troubleshooting

### Erro: "Chave da API OpenAI não configurada"
- Verifique se a variável `OPENAI_API_KEY` está configurada
- Certifique-se de que não há espaços extras

### Erro: "Timeout"
- Render tem timeout de 30 segundos para requests
- Use modelo Whisper menor (`tiny` ou `base`)

### Erro: "Build failed"
- Verifique se todas as dependências estão no `requirements.txt`
- Verifique os logs de build na Render

## 📞 Suporte

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Logs**: Render Dashboard > Logs
- **Status**: [status.render.com](https://status.render.com)

---

**Deploy realizado com ❤️ por Bruno**
"""
    
    try:
        with open("RENDER_DEPLOY.md", "w", encoding="utf-8") as f:
            f.write(instrucoes)
        print("✅ Instruções de deploy criadas!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar instruções: {e}")
        return False


def main():
    """Função principal de preparação para Render"""
    print("Preparando Deploy para Render.com")
    print("=" * 50)
    
    # Verificar arquivos
    if not verificar_arquivos_render():
        print("\n❌ Arquivos necessários não encontrados!")
        return False
    
    # Verificar requirements
    if not verificar_requirements():
        print("\n❌ requirements.txt não está correto!")
        return False
    
    # Criar arquivo .env.example
    criar_arquivo_env_exemplo()
    
    # Testar API localmente
    if not testar_api_localmente():
        print("\n⚠️ API não funcionou localmente, mas continuando...")
    
    # Criar instruções
    criar_instrucoes_deploy()
    
    print("\n🎉 Preparação para Render concluída!")
    print("\n📋 Próximos passos:")
    print("1. Acesse render.com")
    print("2. Conecte o repositório brunofabioo/yt-transcribe")
    print("3. Configure as variáveis de ambiente")
    print("4. Faça o deploy!")
    print("\n📖 Instruções detalhadas em: RENDER_DEPLOY.md")
    
    return True


if __name__ == "__main__":
    main()
