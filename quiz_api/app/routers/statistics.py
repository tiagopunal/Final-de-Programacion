"""
Router para obtener estadísticas y reportes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.database import get_db
from app.models.quiz_session import QuizSession
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/global", response_model=Dict[str, Any])
def estadisticas_globales(db: Session = Depends(get_db)):
    """
    Obtener estadísticas globales del sistema.
    
    Retorna:
    - Total de preguntas activas
    - Total de sesiones completadas
    - Promedio de aciertos general
    - Categorías más difíciles
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        Dict con estadísticas globales
    """
    return QuizService.obtener_estadisticas_globales(db)


@router.get("/session/{session_id}", response_model=Dict[str, Any])
def estadisticas_sesion(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas detalladas de una sesión específica.
    
    Retorna:
    - Puntuación final
    - Porcentaje de aciertos
    - Tiempo promedio por pregunta
    - Resumen detallado de respuestas
    
    Args:
        session_id: ID de la sesión
        db: Sesión de base de datos
        
    Returns:
        Dict con estadísticas de la sesión
        
    Raises:
        HTTPException: Si la sesión no existe
    """
    # Validar que la sesión existe
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    try:
        estadisticas = QuizService.calcular_puntuacion_sesion(db, session_id)
        
        # Agregar información de la sesión
        estadisticas["id_sesion"] = sesion.id
        estadisticas["usuario_nombre"] = sesion.usuario_nombre
        estadisticas["fecha_inicio"] = sesion.fecha_inicio
        estadisticas["fecha_fin"] = sesion.fecha_fin
        estadisticas["estado"] = sesion.estado
        estadisticas["tiempo_total_segundos"] = sesion.tiempo_total_segundos
        
        return estadisticas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/questions/difficult", response_model=List[Dict[str, Any]])
def preguntas_dificiles(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Obtener preguntas con mayor tasa de error.
    
    Retorna:
    - Lista de preguntas ordenadas por tasa de error
    - Incluye cuántas veces fue respondida y cuántas incorrectamente
    
    Args:
        limit: Número máximo de preguntas a retornar
        db: Sesión de base de datos
        
    Returns:
        List[Dict]: Preguntas con mayor tasa de error
    """
    return QuizService.obtener_preguntas_difíciles(db, limit)


@router.get("/categories", response_model=List[Dict[str, Any]])
def rendimiento_por_categoria(db: Session = Depends(get_db)):
    """
    Obtener rendimiento promedio por categoría.
    
    Retorna:
    - Rendimiento promedio por cada categoría
    - Número de preguntas por categoría
    - Aciertos y errores por categoría
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        List[Dict]: Rendimiento por categoría
    """
    return QuizService.obtener_rendimiento_por_categoria(db)
