"""
YouTube Video Transcriber & Summarizer
=====================================

Sistema simplificado para transcrever e resumir vídeos do YouTube usando OpenAI.
Versão otimizada para deploy.

Autor: Bruno
Data: 2024
"""

import yt_dlp
import whisper
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re
import subprocess
from typing import Optional, Dict, Any
import requests
import time
import random

# Importação compatível com diferentes versões do OpenAI
try:
    from openai import OpenAI
    OPENAI_NEW_VERSION = True
except ImportError:
    try:
        import openai
        OPENAI_NEW_VERSION = False
    except ImportError:
        OPENAI_NEW_VERSION = None


class YouTubeTranscriber:
    """
    Classe simplificada para transcrição e resumo de vídeos do YouTube.
    Focada em funcionalidade com OpenAI para máxima qualidade.
    """
    
    def __init__(self, openai_api_key: str, whisper_model_size: str = "base"):
        """
        Inicializa o transcriber.
        
        Args:
            openai_api_key: Chave da API OpenAI (obrigatória)
            whisper_model_size: Tamanho do modelo Whisper ("tiny", "base", "small", "medium", "large")
        """
        if not openai_api_key:
            raise ValueError("Chave da API OpenAI é obrigatória")
        
        self.openai_api_key = openai_api_key
        self.whisper_model_size = whisper_model_size
        self.whisper_model = None
        self.openai_client = None
        
        # Configurar OpenAI
        if OPENAI_NEW_VERSION:
            self.openai_client = OpenAI(api_key=openai_api_key)
        else:
            openai.api_key = openai_api_key
    
    def _extract_video_id(self, url: str) -> str:
        """Extrai o ID do vídeo da URL do YouTube"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError("URL do YouTube inválida")
    
    def get_youtube_transcript(self, video_id: str) -> Optional[str]:
        """
        Tenta obter a transcrição diretamente do YouTube.
        
        Args:
            video_id: ID do vídeo do YouTube
            
        Returns:
            Transcrição em texto ou None se não disponível
        """
        try:
            print("🔍 Obtendo transcrição do YouTube...")
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['pt', 'pt-BR', 'en', 'es']
            )
            
            text = ' '.join([item['text'] for item in transcript])
            print("✅ Transcrição obtida do YouTube!")
            return text
            
        except Exception as e:
            print(f"⚠️ Transcrição do YouTube não disponível: {e}")
            return None
    
    def download_video(self, url: str, output_path: str = "temp_video.mp4") -> str:
        """
        Baixa o vídeo do YouTube usando estratégias anti-bot.
        Tenta em ordem crescente de agressividade.
        """
        print("📥 Baixando vídeo do YouTube...")

        strategies = [
            self._dl_basic,
            self._dl_with_headers,
            self._dl_with_browser_cookies,
            self._dl_with_retries,
        ]

        last_error: Optional[Exception] = None
        for idx, strategy in enumerate(strategies, start=1):
            try:
                print(f"🔄 Estratégia {idx}/{len(strategies)}...")
                strategy(url, output_path)
                print("✅ Vídeo baixado com sucesso!")
                return output_path
            except Exception as err:
                last_error = err
                print(f"⚠️ Falhou estratégia {idx}: {err}")
                if idx < len(strategies):
                    time.sleep(1.5)
                continue

        raise Exception(f"Erro ao baixar vídeo: {last_error}")

    def _common_headers(self) -> Dict[str, str]:
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _dl_basic(self, url: str, output_path: str) -> None:
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best[height<=720]',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def _dl_with_headers(self, url: str, output_path: str) -> None:
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best[height<=720]',
            'quiet': True,
            'http_headers': self._common_headers(),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def _dl_with_browser_cookies(self, url: str, output_path: str) -> None:
        """Tenta usar cookies do navegador local (Chrome/Edge/Firefox)."""
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best[height<=720]',
            'quiet': True,
            'http_headers': self._common_headers(),
            # Tenta diferentes navegadores automaticamente
            'cookiesfrombrowser': ('chrome', 'edge', 'firefox'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def _dl_with_retries(self, url: str, output_path: str) -> None:
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best[height<=720]',
            'quiet': True,
            'http_headers': self._common_headers(),
            'retries': 5,
            'fragment_retries': 5,
            'extractor_retries': 5,
            'throttledratelimit': 1024 * 512,  # 512KB/s para evitar throttling agressivo
        }
        # Pequeno atraso aleatório para disfarçar padrão
        time.sleep(random.uniform(1.0, 2.5))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def extract_audio_ffmpeg(self, video_path: str, audio_path: str) -> None:
        """
        Extrai áudio usando ffmpeg diretamente.
        
        Args:
            video_path: Caminho do vídeo
            audio_path: Caminho para salvar o áudio
        """
        # Verificar se ffmpeg está disponível
        ffmpeg_cmd = "ffmpeg"
        if os.path.exists("ffmpeg.exe"):
            ffmpeg_cmd = "./ffmpeg.exe"
        
        # Comando ffmpeg otimizado para Whisper
        cmd = [
            ffmpeg_cmd,
            "-i", video_path,
            "-vn",  # Sem vídeo
            "-acodec", "pcm_s16le",  # Codec de áudio
            "-ar", "16000",  # Sample rate 16kHz
            "-ac", "1",  # Mono
            "-y",  # Sobrescrever arquivo de saída
            audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro ao executar ffmpeg: {e}")
        except FileNotFoundError:
            raise Exception("FFmpeg não encontrado. Instale o FFmpeg.")
    
    def transcribe_audio_whisper(self, audio_path: str, language: str = "pt") -> str:
        """
        Transcreve áudio usando Whisper.
        
        Args:
            audio_path: Caminho do arquivo de áudio
            language: Idioma do áudio
            
        Returns:
            Texto transcrito
        """
        print("📝 Transcrevendo áudio com Whisper...")
        
        # Carregar modelo se ainda não foi carregado
        if self.whisper_model is None:
            print(f"🔄 Carregando modelo Whisper ({self.whisper_model_size})...")
            self.whisper_model = whisper.load_model(self.whisper_model_size)
        
        try:
            result = self.whisper_model.transcribe(
                audio_path, 
                language=language,
                verbose=False
            )
            print("✅ Transcrição concluída!")
            return result["text"]
            
        except Exception as e:
            raise Exception(f"Erro na transcrição: {e}")
    
    def summarize_with_openai(self, text: str, max_tokens: int = 500) -> str:
        """
        Resume texto usando OpenAI API.
        
        Args:
            text: Texto para resumir
            max_tokens: Número máximo de tokens no resumo
            
        Returns:
            Resumo do texto
        """
        print("🤖 Gerando resumo com OpenAI...")
        
        try:
            if OPENAI_NEW_VERSION and self.openai_client:
                # Nova versão do OpenAI
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Você é um assistente especializado em resumir vídeos de forma clara, concisa e informativa. Mantenha os pontos principais e seja objetivo."
                        },
                        {
                            "role": "user", 
                            "content": f"Resuma o seguinte texto de um vídeo do YouTube em português, destacando os pontos principais:\n\n{text}"
                        }
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                result = response.choices[0].message.content
            else:
                # Versão antiga do OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Você é um assistente especializado em resumir vídeos de forma clara, concisa e informativa. Mantenha os pontos principais e seja objetivo."
                        },
                        {
                            "role": "user", 
                            "content": f"Resuma o seguinte texto de um vídeo do YouTube em português, destacando os pontos principais:\n\n{text}"
                        }
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                result = response.choices[0].message.content
            
            print("✅ Resumo gerado com OpenAI!")
            return result
            
        except Exception as e:
            raise Exception(f"Erro ao gerar resumo com OpenAI: {e}")
    
    def process_video(self, url: str) -> Dict[str, Any]:
        """
        Processa um vídeo completo: transcrição e resumo.
        
        Args:
            url: URL do vídeo do YouTube
            
        Returns:
            Dicionário com transcrição e resumo
        """
        video_id = self._extract_video_id(url)
        temp_files = []
        
        try:
            # 1. Tentar obter transcrição do YouTube primeiro
            transcript = self.get_youtube_transcript(video_id)
            
            # 2. Se não conseguiu transcrição do YouTube, baixar e transcrever
            if not transcript:
                print("🔄 Transcrição do YouTube não disponível, baixando vídeo...")
                
                # Download do vídeo
                video_path = self.download_video(url)
                temp_files.append(video_path)
                
                # Extração do áudio
                audio_path = "temp_audio.wav"
                self.extract_audio_ffmpeg(video_path, audio_path)
                temp_files.append(audio_path)
                
                # Transcrição com Whisper
                transcript = self.transcribe_audio_whisper(audio_path)
            
            # 3. Geração do resumo com OpenAI
            summary = self.summarize_with_openai(transcript)
            
            return {
                "video_id": video_id,
                "transcript": transcript,
                "summary": summary,
                "method": "youtube_transcript" if not temp_files else "whisper",
                "success": True
            }
            
        except Exception as e:
            return {
                "video_id": video_id,
                "error": str(e),
                "success": False
            }
            
        finally:
            # Limpeza dos arquivos temporários
            for file_path in temp_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    pass
    
    def save_results(self, results: Dict[str, Any], output_file: str = "resultado.txt"):
        """
        Salva os resultados em um arquivo.
        
        Args:
            results: Resultados do processamento
            output_file: Nome do arquivo de saída
        """
        if not results["success"]:
            print(f"❌ Erro: {results.get('error', 'Erro desconhecido')}")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("RESUMO DE VÍDEO DO YOUTUBE\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"ID do Vídeo: {results['video_id']}\n")
            f.write(f"Método: {results['method']}\n\n")
            
            f.write("TRANSCRIÇÃO COMPLETA:\n")
            f.write("-"*40 + "\n")
            f.write(results['transcript'])
            f.write("\n\n")
            
            f.write("RESUMO:\n")
            f.write("-"*40 + "\n")
            f.write(results['summary'])
            f.write("\n\n")
        
        print(f"💾 Resultados salvos em: {output_file}")


def main():
    """Função principal para demonstração"""
    print("🎬 YouTube Video Transcriber & Summarizer")
    print("="*50)
    
    # Obter chave da API OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    if not OPENAI_API_KEY:
        print("❌ Chave da API OpenAI não encontrada!")
        print("Configure a variável de ambiente OPENAI_API_KEY")
        print("Exemplo: set OPENAI_API_KEY=sua_chave_aqui")
        return
    
    # Inicializar transcriber
    transcriber = YouTubeTranscriber(
        openai_api_key=OPENAI_API_KEY,
        whisper_model_size="base"
    )
    
    # URL do vídeo
    video_url = input("Digite a URL do vídeo do YouTube: ").strip()
    
    if not video_url:
        print("❌ URL não fornecida!")
        return
    
    # Processar vídeo
    print(f"\n🚀 Processando vídeo: {video_url}")
    results = transcriber.process_video(video_url)
    
    # Exibir resultados
    if results["success"]:
        print("\n" + "="*60)
        print("📝 TRANSCRIÇÃO:")
        print("="*60)
        print(results["transcript"][:500] + "..." if len(results["transcript"]) > 500 else results["transcript"])
        
        print("\n" + "="*60)
        print("📄 RESUMO:")
        print("="*60)
        print(results["summary"])
        
        # Salvar resultados
        transcriber.save_results(results)
        
    else:
        print(f"❌ Erro: {results.get('error', 'Erro desconhecido')}")


if __name__ == "__main__":
    main()