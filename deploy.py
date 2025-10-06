"""
Script de Deploy - YouTube Video Transcriber
===========================================

Script para configurar e preparar o ambiente para deploy.
"""

import subprocess
import sys
import os
from pathlib import Path


def verificar_python():
    """Verifica se o Python está instalado"""
    print("🐍 Verificando Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado!")
    return True


def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def verificar_ffmpeg():
    """Verifica se o FFmpeg está disponível"""
    print("\n🔍 Verificando FFmpeg...")
    
    # Verificar se ffmpeg.exe está no diretório atual
    if os.path.exists("ffmpeg.exe"):
        print("✅ FFmpeg encontrado no diretório atual!")
        return True
    
    # Verificar se ffmpeg está no PATH
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg encontrado no PATH!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ FFmpeg não encontrado!")
        print("📥 Baixando FFmpeg...")
        return baixar_ffmpeg()


def baixar_ffmpeg():
    """Baixa o FFmpeg se necessário"""
    try:
        import requests
        import zipfile
        
        # URL do FFmpeg para Windows
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        
        print("📥 Baixando FFmpeg...")
        response = requests.get(url, stream=True)
        
        with open("ffmpeg.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("📦 Extraindo FFmpeg...")
        with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Mover ffmpeg.exe para o diretório atual
        for root, dirs, files in os.walk("."):
            if "ffmpeg.exe" in files:
                os.rename(os.path.join(root, "ffmpeg.exe"), "ffmpeg.exe")
                break
        
        # Limpar arquivos temporários
        os.remove("ffmpeg.zip")
        
        print("✅ FFmpeg instalado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao baixar FFmpeg: {e}")
        print("💡 Instale o FFmpeg manualmente: https://ffmpeg.org/download.html")
        return False


def configurar_ambiente():
    """Configura o ambiente de desenvolvimento"""
    print("\n⚙️ Configurando ambiente...")
    
    # Criar arquivo .env se não existir
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Criando arquivo .env...")
        with open(env_file, "w") as f:
            f.write("# YouTube Video Transcriber & Summarizer\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("WHISPER_MODEL_SIZE=base\n")
            f.write("LANGUAGE=pt\n")
        print("✅ Arquivo .env criado!")
        print("⚠️ Configure sua chave da API OpenAI no arquivo .env")
    
    # Criar diretório para resultados
    results_dir = Path("resultados")
    results_dir.mkdir(exist_ok=True)
    print("📁 Diretório 'resultados' criado!")


def testar_instalacao():
    """Testa se a instalação está funcionando"""
    print("\n🧪 Testando instalação...")
    
    try:
        from youtube_transcriber import YouTubeTranscriber
        print("✅ YouTubeTranscriber importado com sucesso")
        
        # Teste básico (sem chave da API)
        try:
            transcriber = YouTubeTranscriber(openai_api_key="test")
            print("✅ YouTubeTranscriber inicializado com sucesso")
        except ValueError:
            print("✅ YouTubeTranscriber validando chave da API corretamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def main():
    """Função principal de deploy"""
    print("🚀 Deploy - YouTube Video Transcriber")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        return False
    
    # Instalar dependências
    if not instalar_dependencias():
        print("\n❌ Falha na instalação das dependências!")
        return False
    
    # Verificar FFmpeg
    ffmpeg_ok = verificar_ffmpeg()
    
    # Configurar ambiente
    configurar_ambiente()
    
    # Testar instalação
    if not testar_instalacao():
        print("\n❌ Falha no teste da instalação!")
        return False
    
    print("\n🎉 Deploy concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure sua chave da API OpenAI no arquivo .env")
    print("2. Execute: python app.py")
    print("3. Ou execute: python youtube_transcriber.py")
    
    if not ffmpeg_ok:
        print("\n⚠️ ATENÇÃO: FFmpeg não está disponível!")
        print("   Algumas funcionalidades podem não funcionar.")
        print("   Instale o FFmpeg manualmente se necessário.")
    
    print("\n🔑 Para obter sua chave da API OpenAI:")
    print("   https://platform.openai.com/api-keys")
    
    return True


if __name__ == "__main__":
    main()
