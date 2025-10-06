"""
YouTube Video Transcriber API
============================

API FastAPI para transcrever e resumir vídeos do YouTube.
Otimizada para deploy na Vercel.

Endpoints:
- POST /transcribe - Transcrever e resumir vídeo
- GET /health - Health check
- GET / - Documentação da API
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import os
import asyncio
from youtube_transcriber import YouTubeTranscriber
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="YouTube Video Transcriber API",
    description="API para transcrever e resumir vídeos do YouTube usando OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class VideoRequest(BaseModel):
    url: HttpUrl
    whisper_model_size: Optional[str] = "base"
    language: Optional[str] = "pt"
    max_tokens: Optional[int] = 500

class VideoResponse(BaseModel):
    success: bool
    video_id: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    method: Optional[str] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

# Variáveis globais
transcriber_instance = None

def get_transcriber():
    """Obtém instância do transcriber (singleton)"""
    global transcriber_instance
    
    if transcriber_instance is None:
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            raise HTTPException(
                status_code=500, 
                detail="Chave da API OpenAI não configurada"
            )
        
        transcriber_instance = YouTubeTranscriber(
            openai_api_key=openai_key,
            whisper_model_size="base"
        )
    
    return transcriber_instance

@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "YouTube Video Transcriber API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Verificar se a chave da API está configurada
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            return HealthResponse(
                status="error",
                message="Chave da API OpenAI não configurada",
                version="1.0.0"
            )
        
        return HealthResponse(
            status="healthy",
            message="API funcionando corretamente",
            version="1.0.0"
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=f"Erro: {str(e)}",
            version="1.0.0"
        )

@app.post("/transcribe", response_model=VideoResponse)
async def transcribe_video(request: VideoRequest):
    """
    Transcreve e resume um vídeo do YouTube
    
    Args:
        request: Dados da requisição com URL do vídeo
        
    Returns:
        Resposta com transcrição e resumo
    """
    import time
    start_time = time.time()
    
    try:
        logger.info(f"Processando vídeo: {request.url}")
        
        # Obter instância do transcriber
        transcriber = get_transcriber()
        
        # Processar vídeo
        results = transcriber.process_video(str(request.url))
        
        processing_time = time.time() - start_time
        
        if results["success"]:
            logger.info(f"Vídeo processado com sucesso em {processing_time:.2f}s")
            
            return VideoResponse(
                success=True,
                video_id=results["video_id"],
                transcript=results["transcript"],
                summary=results["summary"],
                method=results["method"],
                processing_time=processing_time
            )
        else:
            logger.error(f"Erro ao processar vídeo: {results.get('error')}")
            
            return VideoResponse(
                success=False,
                video_id=results.get("video_id", "unknown"),
                error=results.get("error", "Erro desconhecido"),
                processing_time=processing_time
            )
            
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Erro inesperado: {str(e)}")
        
        return VideoResponse(
            success=False,
            video_id="unknown",
            error=f"Erro interno: {str(e)}",
            processing_time=processing_time
        )

@app.post("/transcribe-async", response_model=Dict[str, str])
async def transcribe_video_async(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Inicia processamento assíncrono de vídeo (para vídeos longos)
    
    Args:
        request: Dados da requisição com URL do vídeo
        background_tasks: Tarefas em background do FastAPI
        
    Returns:
        ID da tarefa para consulta posterior
    """
    import uuid
    task_id = str(uuid.uuid4())
    
    # Adicionar tarefa em background
    background_tasks.add_task(process_video_background, task_id, str(request.url))
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "Vídeo sendo processado em background"
    }

async def process_video_background(task_id: str, video_url: str):
    """Processa vídeo em background"""
    try:
        transcriber = get_transcriber()
        results = transcriber.process_video(video_url)
        
        # Aqui você poderia salvar os resultados em um banco de dados
        # ou cache para consulta posterior via task_id
        logger.info(f"Tarefa {task_id} concluída: {results['success']}")
        
    except Exception as e:
        logger.error(f"Erro na tarefa {task_id}: {str(e)}")

# Handler para Vercel
def handler(request):
    """Handler para Vercel"""
    return app

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
