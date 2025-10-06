"""
Teste da YouTube Video Transcriber API
=====================================

Script para testar a API localmente ou em produção.
"""

import requests
import json
import time
from typing import Dict, Any


def test_health_check(base_url: str) -> bool:
    """Testa o health check da API"""
    print("🔍 Testando health check...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"📝 Mensagem: {data.get('message')}")
        print(f"🔢 Versão: {data.get('version')}")
        
        return data.get('status') == 'healthy'
        
    except requests.RequestException as e:
        print(f"❌ Erro no health check: {e}")
        return False


def test_transcribe_video(base_url: str, video_url: str) -> Dict[str, Any]:
    """Testa a transcrição de vídeo"""
    print(f"\n🎬 Testando transcrição de vídeo...")
    print(f"URL: {video_url}")
    
    payload = {
        "url": video_url,
        "whisper_model_size": "base",
        "language": "pt",
        "max_tokens": 300
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/transcribe",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minutos de timeout
        )
        processing_time = time.time() - start_time
        
        response.raise_for_status()
        data = response.json()
        
        print(f"⏱️ Tempo de processamento: {processing_time:.2f}s")
        print(f"✅ Sucesso: {data.get('success')}")
        
        if data.get('success'):
            print(f"📹 ID do Vídeo: {data.get('video_id')}")
            print(f"🔧 Método: {data.get('method')}")
            print(f"📄 Resumo: {data.get('summary', 'N/A')[:200]}...")
            print(f"📝 Transcrição: {data.get('transcript', 'N/A')[:200]}...")
        else:
            print(f"❌ Erro: {data.get('error')}")
        
        return data
        
    except requests.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return {"error": str(e)}


def test_async_transcribe(base_url: str, video_url: str) -> Dict[str, Any]:
    """Testa a transcrição assíncrona"""
    print(f"\n🔄 Testando transcrição assíncrona...")
    
    payload = {"url": video_url}
    
    try:
        response = requests.post(
            f"{base_url}/transcribe-async",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Tarefa criada: {data.get('task_id')}")
        print(f"📝 Status: {data.get('status')}")
        print(f"💬 Mensagem: {data.get('message')}")
        
        return data
        
    except requests.RequestException as e:
        print(f"❌ Erro na requisição assíncrona: {e}")
        return {"error": str(e)}


def test_api_endpoints(base_url: str):
    """Testa todos os endpoints da API"""
    print("🧪 Testando endpoints da API")
    print("=" * 50)
    
    # Teste 1: Health check
    if not test_health_check(base_url):
        print("\n❌ API não está funcionando. Verifique se está rodando.")
        return
    
    # Teste 2: Endpoint raiz
    print("\n🏠 Testando endpoint raiz...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Resposta: {data}")
    except requests.RequestException as e:
        print(f"❌ Erro: {e}")
    
    # Teste 3: Transcrição de vídeo
    video_url = input("\nDigite a URL do vídeo para testar (ou Enter para pular): ").strip()
    
    if video_url:
        result = test_transcribe_video(base_url, video_url)
        
        if result.get('success'):
            print("\n✅ Teste de transcrição passou!")
        else:
            print("\n❌ Teste de transcrição falhou!")
    
    # Teste 4: Transcrição assíncrona
    if video_url:
        test_async_transcribe(base_url, video_url)
    
    print("\n🎉 Testes concluídos!")


def main():
    """Função principal"""
    print("🎬 Teste da YouTube Video Transcriber API")
    print("=" * 50)
    
    # Configurar URL base
    base_url = input("Digite a URL da API (ou Enter para localhost:8000): ").strip()
    if not base_url:
        base_url = "http://localhost:8000"
    
    print(f"🔗 Testando API em: {base_url}")
    
    # Executar testes
    test_api_endpoints(base_url)


if __name__ == "__main__":
    main()
