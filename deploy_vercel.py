"""
Script de Deploy para Vercel
===========================

Script para configurar e fazer deploy da API na Vercel.
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def verificar_vercel_cli():
    """Verifica se o Vercel CLI está instalado"""
    print("🔍 Verificando Vercel CLI...")
    
    try:
        result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ Vercel CLI não encontrado!")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI não encontrado!")
        return False


def instalar_vercel_cli():
    """Instala o Vercel CLI"""
    print("📦 Instalando Vercel CLI...")
    
    try:
        subprocess.check_call(["npm", "install", "-g", "vercel"])
        print("✅ Vercel CLI instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar Vercel CLI: {e}")
        return False


def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    print("🔍 Verificando arquivos necessários...")
    
    arquivos_necessarios = [
        "main.py",
        "youtube_transcriber.py", 
        "vercel.json",
        "requirements.txt"
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


def configurar_vercel():
    """Configura o projeto para Vercel"""
    print("⚙️ Configurando projeto para Vercel...")
    
    # Verificar se já existe configuração
    if Path(".vercel").exists():
        print("⚠️ Projeto já configurado para Vercel")
        resposta = input("Continuar mesmo assim? (s/N): ").strip().lower()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            return False
    
    try:
        # Fazer login na Vercel
        print("🔐 Fazendo login na Vercel...")
        subprocess.run(["vercel", "login"], check=True)
        
        # Inicializar projeto
        print("🚀 Inicializando projeto...")
        subprocess.run(["vercel", "init"], check=True)
        
        print("✅ Projeto configurado para Vercel!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar Vercel: {e}")
        return False


def configurar_variaveis_ambiente():
    """Configura variáveis de ambiente na Vercel"""
    print("🔧 Configurando variáveis de ambiente...")
    
    openai_key = input("Digite sua chave da API OpenAI: ").strip()
    
    if not openai_key:
        print("⚠️ Chave da API OpenAI não fornecida!")
        print("Configure manualmente na Vercel Dashboard:")
        print("1. Vá para Settings > Environment Variables")
        print("2. Adicione: OPENAI_API_KEY = sua_chave_aqui")
        return False
    
    try:
        # Adicionar variável de ambiente
        subprocess.run([
            "vercel", "env", "add", "OPENAI_API_KEY", 
            "production", openai_key
        ], check=True)
        
        print("✅ Variável de ambiente configurada!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar variável de ambiente: {e}")
        print("Configure manualmente na Vercel Dashboard")
        return False


def fazer_deploy():
    """Faz deploy da API na Vercel"""
    print("🚀 Fazendo deploy na Vercel...")
    
    try:
        # Deploy
        result = subprocess.run(["vercel", "--prod"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deploy realizado com sucesso!")
            print(f"📝 Output: {result.stdout}")
            
            # Extrair URL do output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and 'vercel.app' in line:
                    print(f"🌐 URL da API: {line.strip()}")
                    break
            
            return True
        else:
            print(f"❌ Erro no deploy: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no deploy: {e}")
        return False


def testar_deploy(url: str):
    """Testa se o deploy está funcionando"""
    print(f"\n🧪 Testando deploy em: {url}")
    
    try:
        import requests
        
        # Teste health check
        response = requests.get(f"{url}/health", timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if data.get('status') == 'healthy':
            print("✅ API está funcionando corretamente!")
            print(f"📝 Mensagem: {data.get('message')}")
            return True
        else:
            print(f"❌ API não está funcionando: {data.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        return False


def main():
    """Função principal de deploy"""
    print("🚀 Deploy da YouTube Video Transcriber API na Vercel")
    print("=" * 60)
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n❌ Arquivos necessários não encontrados!")
        return False
    
    # Verificar/instalar Vercel CLI
    if not verificar_vercel_cli():
        if not instalar_vercel_cli():
            print("\n❌ Não foi possível instalar Vercel CLI!")
            print("Instale manualmente: npm install -g vercel")
            return False
    
    # Configurar Vercel
    if not configurar_vercel():
        print("\n❌ Falha na configuração do Vercel!")
        return False
    
    # Configurar variáveis de ambiente
    configurar_variaveis_ambiente()
    
    # Fazer deploy
    if not fazer_deploy():
        print("\n❌ Falha no deploy!")
        return False
    
    print("\n🎉 Deploy concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Teste a API usando: python test_api.py")
    print("2. Acesse a documentação em: https://seu-projeto.vercel.app/docs")
    print("3. Configure domínio personalizado se necessário")
    
    return True


if __name__ == "__main__":
    main()
