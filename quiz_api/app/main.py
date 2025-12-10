"""
Aplicación FastAPI principal para Quiz API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.database import init_db
from app.routers import questions, quiz_sessions, answers, statistics

# Inicializar FastAPI app
app = FastAPI(
    title="Quiz API REST",
    description="API REST para Quiz Interactivo con FastAPI, SQLAlchemy y SQLite",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de startup
@app.on_event("startup")
def startup_event():
    """Inicializar la base de datos cuando arranca la aplicación"""
    init_db()
    print("✓ Base de datos inicializada")


# Incluir routers
app.include_router(questions.router)
app.include_router(quiz_sessions.router)
app.include_router(answers.router)
app.include_router(statistics.router)

# Servir archivos estáticos del frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


# Ruta para servir el HTML principal
@app.get("/", tags=["root"], include_in_schema=False)
async def root():
    """
    Sirve la página principal del frontend.
    """
    html_file = frontend_path / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return {
        "mensaje": "Bienvenido a Quiz API",
        "version": "1.0.0",
        "documentacion": "/docs",
        "endpoints": {
            "preguntas": "/questions",
            "sesiones": "/quiz-sessions",
            "respuestas": "/answers",
            "estadisticas": "/statistics"
        }
    }


@app.get("/health", tags=["root"])
def health_check():
    """
    Verificar el estado de la API.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
