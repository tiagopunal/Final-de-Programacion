"""
Router para gestionar sesiones de quiz
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.quiz_session import QuizSession
from app.schemas.quiz_session import (
    QuizSessionCreate, QuizSessionResponse, QuizSessionUpdate, QuizSessionComplete
)
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz-sessions", tags=["quiz-sessions"])


@router.post("/", response_model=QuizSessionResponse, status_code=201)
def iniciar_sesion(
    sesion: QuizSessionCreate,
    db: Session = Depends(get_db)
):
    """
    Iniciar una nueva sesión de quiz.
    
    Args:
        sesion: Datos de la sesión
        db: Sesión de base de datos
        
    Returns:
        QuizSessionResponse: La sesión creada
    """
    db_sesion = QuizSession(
        usuario_nombre=sesion.usuario_nombre,
        estado="en_progreso"
    )
    db.add(db_sesion)
    db.commit()
    db.refresh(db_sesion)
    return db_sesion


@router.get("/", response_model=List[QuizSessionResponse])
def listar_sesiones(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    estado: str = Query(None, description="Filtrar por estado (en_progreso, completado, abandonado)"),
    db: Session = Depends(get_db)
):
    """
    Listar sesiones de quiz con paginación.
    
    Args:
        skip: Número de registros a saltar
        limit: Límite de registros
        estado: Filtrar por estado (opcional)
        db: Sesión de base de datos
        
    Returns:
        List[QuizSessionResponse]: Lista de sesiones
    """
    query = db.query(QuizSession)
    
    if estado:
        query = query.filter(QuizSession.estado == estado)
    
    sesiones = query.offset(skip).limit(limit).all()
    return sesiones


@router.get("/{session_id}", response_model=QuizSessionResponse)
def obtener_sesion(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de una sesión específica.
    
    Args:
        session_id: ID de la sesión
        db: Sesión de base de datos
        
    Returns:
        QuizSessionResponse: Detalles de la sesión
        
    Raises:
        HTTPException: Si la sesión no existe
    """
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return sesion


@router.put("/{session_id}/complete", response_model=QuizSessionResponse)
def completar_sesion(
    session_id: int,
    complete_data: QuizSessionComplete,
    db: Session = Depends(get_db)
):
    """
    Finalizar sesión y calcular puntuación final.
    
    Args:
        session_id: ID de la sesión
        complete_data: Datos de finalización (tiempo total opcional)
        db: Sesión de base de datos
        
    Returns:
        QuizSessionResponse: Sesión completada con puntuación
        
    Raises:
        HTTPException: Si la sesión no existe
    """
    try:
        sesion = QuizService.completar_sesion(
            db,
            session_id,
            complete_data.tiempo_total_segundos
        )
        return sesion
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{session_id}", status_code=204)
def eliminar_sesion(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una sesión de quiz.
    
    Args:
        session_id: ID de la sesión
        db: Sesión de base de datos
        
    Raises:
        HTTPException: Si la sesión no existe
    """
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    db.delete(sesion)
    db.commit()
