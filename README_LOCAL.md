# 📼 Transcrição Local (CLI)

Scripts para executar a transcrição local do YouTube, reutilizando a lógica do projeto de API.

## Requisitos
- Python 3.8+
- ffmpeg disponível (ou ffmpeg.exe no diretório do projeto)
- Dependências já listadas no requirements.txt

Instale:
```
pip install -r requirements.txt
```

## Uso

```
python -m local.transcribe --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --openai-key "sk-..." \
  --model base \
  --out resultados/resultado.txt
```

Parâmetros:
- --url (obrigatório): link do vídeo do YouTube
- --openai-key (opcional): chave para gerar resumo com OpenAI; sem ela só transcreve
- --model (opcional): modelo do Whisper: tiny|base|small|medium|large (padrão: base)
- --out (opcional): arquivo de saída (padrão: resultados/resultado.txt)

## Notas
- O script tenta usar a transcrição nativa do YouTube antes de baixar o vídeo.
- Se precisar baixar, usa yt-dlp com estratégias anti-bot.
- Em casos de bloqueio do YouTube, abrir o Chrome logado ajuda, pois o yt-dlp pode ler cookies do navegador.

## Exemplos

Apenas transcrever (sem OpenAI):
```
python -m local.transcribe --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Transcrever e resumir com OpenAI:
```
python -m local.transcribe --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --openai-key "sk-..."
```

Resultado será salvo em resultados/resultado.txt.
