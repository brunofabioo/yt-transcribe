"""
Cliente para a YouTube Video Transcriber API
==========================================

Exemplo de como usar a API para transcrever vídeos.
"""

import requests
import json
from typing import Dict, Any


class YouTubeTranscriberClient:
    """Cliente para a API de transcrição de vídeos do YouTube"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inicializa o cliente
        
        Args:
            base_url: URL base da API
        """
        self.base_url = base_url.rstrip('/')
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica se a API está funcionando"""
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def transcribe_video(self, url: str, whisper_model_size: str = "base", 
                        language: str = "pt", max_tokens: int = 500) -> Dict[str, Any]:
        """
        Transcreve e resume um vídeo do YouTube
        
        Args:
            url: URL do vídeo do YouTube
            whisper_model_size: Tamanho do modelo Whisper
            language: Idioma para transcrição
            max_tokens: Número máximo de tokens no resumo
            
        Returns:
            Resposta da API com transcrição e resumo
        """
        try:
            payload = {
                "url": url,
                "whisper_model_size": whisper_model_size,
                "language": language,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/transcribe",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def transcribe_video_async(self, url: str) -> Dict[str, Any]:
        """
        Inicia processamento assíncrono de vídeo
        
        Args:
            url: URL do vídeo do YouTube
            
        Returns:
            ID da tarefa para consulta posterior
        """
        try:
            payload = {"url": url}
            
            response = requests.post(
                f"{self.base_url}/transcribe-async",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            return {"error": str(e)}


def main():
    """Exemplo de uso do cliente"""
    print("🎬 Cliente da YouTube Video Transcriber API")
    print("=" * 50)
    
    # Inicializar cliente
    client = YouTubeTranscriberClient()
    
    # Verificar saúde da API
    print("🔍 Verificando API...")
    health = client.health_check()
    print(f"Status: {health.get('status', 'unknown')}")
    print(f"Mensagem: {health.get('message', 'N/A')}")
    
    if health.get('status') != 'healthy':
        print("❌ API não está funcionando corretamente!")
        return
    
    # Exemplo de transcrição
    video_url = input("\nDigite a URL do vídeo do YouTube: ").strip()
    
    if not video_url:
        print("❌ URL não fornecida!")
        return
    
    print(f"\n🚀 Processando vídeo: {video_url}")
    
    # Transcrever vídeo
    result = client.transcribe_video(video_url)
    
    if result.get('success'):
        print("\n✅ Vídeo processado com sucesso!")
        print(f"📹 ID do Vídeo: {result['video_id']}")
        print(f"⏱️ Tempo de Processamento: {result.get('processing_time', 0):.2f}s")
        print(f"🔧 Método: {result.get('method', 'unknown')}")
        
        print("\n" + "="*60)
        print("📄 RESUMO:")
        print("="*60)
        print(result.get('summary', 'N/A'))
        
        print("\n" + "="*60)
        print("📝 TRANSCRIÇÃO (primeiros 500 caracteres):")
        print("="*60)
        transcript = result.get('transcript', '')
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        
    else:
        print(f"\n❌ Erro: {result.get('error', 'Erro desconhecido')}")


if __name__ == "__main__":
    main()
