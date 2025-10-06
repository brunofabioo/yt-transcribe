"""
YouTube Video Transcriber & Summarizer - App Principal
=====================================================

Aplicação simplificada para transcrever e resumir vídeos do YouTube.
Versão otimizada para deploy.

Uso:
    python app.py

Requisitos:
    - Chave da API OpenAI configurada
    - FFmpeg instalado
"""

from youtube_transcriber import YouTubeTranscriber
import os
import sys


def main():
    """Função principal da aplicação"""
    print("🎬 YouTube Video Transcriber & Summarizer")
    print("=" * 50)
    
    # Verificar chave da API OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    if not OPENAI_API_KEY:
        print("❌ Chave da API OpenAI não encontrada!")
        print("\n📋 Como configurar:")
        print("1. Obtenha sua chave em: https://platform.openai.com/api-keys")
        print("2. Configure a variável de ambiente:")
        print("   Windows: set OPENAI_API_KEY=sua_chave_aqui")
        print("   Linux/Mac: export OPENAI_API_KEY=sua_chave_aqui")
        print("3. Ou crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")
        return
    
    try:
        # Inicializar transcriber
        print("🔄 Inicializando sistema...")
        transcriber = YouTubeTranscriber(
            openai_api_key=OPENAI_API_KEY,
            whisper_model_size="base"  # Modelo balanceado
        )
        print("✅ Sistema inicializado!")
        
        # Loop principal
        while True:
            print("\n" + "="*50)
            print("📺 PROCESSAR VÍDEO DO YOUTUBE")
            print("="*50)
            
            # Obter URL do vídeo
            video_url = input("\nDigite a URL do vídeo (ou 'sair' para encerrar): ").strip()
            
            if video_url.lower() in ['sair', 'exit', 'quit', '']:
                print("👋 Até logo!")
                break
            
            # Validar URL
            if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
                print("❌ URL inválida! Use uma URL do YouTube.")
                continue
            
            # Processar vídeo
            print(f"\n🚀 Processando vídeo...")
            print(f"URL: {video_url}")
            
            try:
                results = transcriber.process_video(video_url)
                
                if results["success"]:
                    print("\n✅ Processamento concluído com sucesso!")
                    
                    # Exibir resumo
                    print("\n" + "="*60)
                    print("📄 RESUMO:")
                    print("="*60)
                    print(results["summary"])
                    
                    # Salvar resultados
                    output_file = f"resultado_{results['video_id']}.txt"
                    transcriber.save_results(results, output_file)
                    
                    # Perguntar se quer ver transcrição completa
                    ver_transcricao = input("\nVer transcrição completa? (s/N): ").strip().lower()
                    if ver_transcricao in ['s', 'sim', 'y', 'yes']:
                        print("\n" + "="*60)
                        print("📝 TRANSCRIÇÃO COMPLETA:")
                        print("="*60)
                        print(results["transcript"])
                    
                else:
                    print(f"\n❌ Erro: {results.get('error', 'Erro desconhecido')}")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Operação cancelada pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
            
            # Perguntar se quer processar outro vídeo
            continuar = input("\nProcessar outro vídeo? (S/n): ").strip().lower()
            if continuar in ['n', 'não', 'no']:
                print("👋 Até logo!")
                break
    
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação encerrada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
