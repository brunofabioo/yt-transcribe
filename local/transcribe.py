"""
CLI - Transcrição local de vídeos do YouTube
============================================

Uso:
    python -m local.transcribe --url "https://www.youtube.com/watch?v=VIDEO_ID" [--openai-key x] [--model base]

Observações:
    - Reaproveita a classe `YouTubeTranscriber` do projeto.
    - Quando possível, usa a transcrição nativa do YouTube (mais rápida).
    - Se não houver transcrição no YouTube, baixa o vídeo e transcreve via Whisper local.
    - O resumo usa OpenAI se `--openai-key` for passado; caso contrário, apenas transcreve.
"""

import argparse
import os
from pathlib import Path
from typing import Optional

from youtube_transcriber import YouTubeTranscriber


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcrição local de vídeo do YouTube")
    parser.add_argument("--url", required=True, help="URL do vídeo do YouTube")
    parser.add_argument("--openai-key", dest="openai_key", default=os.getenv("OPENAI_API_KEY"), help="Chave da API OpenAI (opcional para resumo)")
    parser.add_argument("--model", dest="whisper_model", default=os.getenv("WHISPER_MODEL_SIZE", "base"), help="Modelo Whisper (tiny|base|small|medium|large)")
    parser.add_argument("--out", dest="output", default="resultados/resultado.txt", help="Arquivo de saída para salvar o resultado")
    return parser.parse_args()


def ensure_output_dir(output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()

    if args.openai_key:
        transcriber = YouTubeTranscriber(openai_api_key=args.openai_key, whisper_model_size=args.whisper_model)
        use_openai = True
    else:
        # Passa uma chave fake somente para cumprir a assinatura; o resumo usará OpenAI apenas se a chave existir
        transcriber = YouTubeTranscriber(openai_api_key="dummy", whisper_model_size=args.whisper_model)
        transcriber.openai_api_key = None  # Desabilita resumo com OpenAI
        use_openai = False

    print("\n🚀 Iniciando transcrição local...")
    print(f"URL: {args.url}")
    print(f"Whisper: {args.whisper_model}")
    print(f"Resumo com OpenAI: {'Sim' if use_openai else 'Não'}")

    results = transcriber.process_video(args.url)

    if not results.get("success"):
        print(f"\n❌ Erro: {results.get('error', 'Erro desconhecido')}")
        return

    ensure_output_dir(args.output)
    transcriber.save_results(results, args.output)

    print("\n✅ Concluído!")
    print(f"💾 Resultado salvo em: {args.output}")
    print("\nResumo (prévia):\n" + results["summary"][:350] + ("..." if len(results["summary"]) > 350 else ""))


if __name__ == "__main__":
    main()


