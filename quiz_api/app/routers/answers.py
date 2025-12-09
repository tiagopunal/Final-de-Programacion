"""
Router para gestionar respuestas
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.answer import Answer
from app.models.question import Question
from app.models.quiz_session import QuizSession
from app.schemas.answer import (
    AnswerCreate, AnswerResponse, AnswerUpdate, AnswerDetailResponse
)
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post("/", response_model=AnswerResponse, status_code=201)
def registrar_respuesta(
    respuesta: AnswerCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar una respuesta del usuario.
    
    Args:
        respuesta: Datos de la respuesta
        db: Sesión de base de datos
        
    Returns:
        AnswerResponse: Respuesta registrada
        
    Raises:
        HTTPException: Si hay errores de validación
    """
    # Validar que la sesión existe
    sesion = db.query(QuizSession).filter(QuizSession.id == respuesta.quiz_session_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    # Validar que la pregunta existe
    pregunta = db.query(Question).filter(Question.id == respuesta.question_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    # Validar que la respuesta no está fuera de rango
    if respuesta.respuesta_seleccionada < 0 or respuesta.respuesta_seleccionada >= len(pregunta.opciones):
        raise HTTPException(
            status_code=400,
            detail=f"Respuesta debe estar entre 0 y {len(pregunta.opciones) - 1}"
        )
    
    # Validar que no hay respuesta duplicada
    if QuizService.verificar_respuesta_duplicada(db, respuesta.quiz_session_id, respuesta.question_id):
        raise HTTPException(
            status_code=400,
            detail="Ya has respondido esta pregunta en esta sesión"
        )
    
    # Validar si la respuesta es correcta
    try:
        es_correcta = QuizService.validar_respuesta(db, respuesta.question_id, respuesta.respuesta_seleccionada)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Crear respuesta
    db_respuesta = Answer(
        quiz_session_id=respuesta.quiz_session_id,
        question_id=respuesta.question_id,
        respuesta_seleccionada=respuesta.respuesta_seleccionada,
        es_correcta=es_correcta,
        tiempo_respuesta_segundos=respuesta.tiempo_respuesta_segundos
    )
    
    db.add(db_respuesta)
    db.commit()
    db.refresh(db_respuesta)
    
    return db_respuesta


@router.get("/session/{session_id}", response_model=List[AnswerDetailResponse])
def obtener_respuestas_sesion(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las respuestas de una sesión específica.
    
    Args:
        session_id: ID de la sesión
        db: Sesión de base de datos
        
    Returns:
        List[AnswerDetailResponse]: Lista de respuestas con detalles
        
    Raises:
        HTTPException: Si la sesión no existe
    """
    # Validar que la sesión existe
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    respuestas = db.query(Answer).filter(Answer.quiz_session_id == session_id).all()
    
    # Mapear a AnswerDetailResponse
    resultado = []
    for respuesta in respuestas:
        pregunta = db.query(Question).filter(Question.id == respuesta.question_id).first()
        
        detalle = AnswerDetailResponse(
            id=respuesta.id,
            quiz_session_id=respuesta.quiz_session_id,
            question_id=respuesta.question_id,
            respuesta_seleccionada=respuesta.respuesta_seleccionada,
            es_correcta=respuesta.es_correcta,
            tiempo_respuesta_segundos=respuesta.tiempo_respuesta_segundos,
            created_at=respuesta.created_at,
            pregunta_texto=pregunta.pregunta if pregunta else None,
            opciones=pregunta.opciones if pregunta else None,
            respuesta_correcta_indice=pregunta.respuesta_correcta if pregunta else None,
            respuesta_seleccionada_texto=pregunta.opciones[respuesta.respuesta_seleccionada] if pregunta else None
        )
        resultado.append(detalle)
    
    return resultado


@router.get("/{answer_id}", response_model=AnswerDetailResponse)
def obtener_respuesta(
    answer_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de una respuesta específica.
    
    Args:
        answer_id: ID de la respuesta
        db: Sesión de base de datos
        
    Returns:
        AnswerDetailResponse: Detalles de la respuesta
        
    Raises:
        HTTPException: Si la respuesta no existe
    """
    respuesta = db.query(Answer).filter(Answer.id == answer_id).first()
    
    if not respuesta:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    pregunta = db.query(Question).filter(Question.id == respuesta.question_id).first()
    
    detalle = AnswerDetailResponse(
        id=respuesta.id,
        quiz_session_id=respuesta.quiz_session_id,
        question_id=respuesta.question_id,
        respuesta_seleccionada=respuesta.respuesta_seleccionada,
        es_correcta=respuesta.es_correcta,
        tiempo_respuesta_segundos=respuesta.tiempo_respuesta_segundos,
        created_at=respuesta.created_at,
        pregunta_texto=pregunta.pregunta if pregunta else None,
        opciones=pregunta.opciones if pregunta else None,
        respuesta_correcta_indice=pregunta.respuesta_correcta if pregunta else None,
        respuesta_seleccionada_texto=pregunta.opciones[respuesta.respuesta_seleccionada] if pregunta else None
    )
    
    return detalle


@router.put("/{answer_id}", response_model=AnswerResponse)
def actualizar_respuesta(
    answer_id: int,
    respuesta_update: AnswerUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una respuesta (para correcciones).
    
    Args:
        answer_id: ID de la respuesta
        respuesta_update: Datos a actualizar
        db: Sesión de base de datos
        
    Returns:
        AnswerResponse: Respuesta actualizada
        
    Raises:
        HTTPException: Si la respuesta no existe o hay errores de validación
    """
    respuesta = db.query(Answer).filter(Answer.id == answer_id).first()
    
    if not respuesta:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    pregunta = db.query(Question).filter(Question.id == respuesta.question_id).first()
    
    # Si se actualiza la respuesta seleccionada, validar el rango y recalcular si es correcta
    if respuesta_update.respuesta_seleccionada is not None:
        if respuesta_update.respuesta_seleccionada < 0 or respuesta_update.respuesta_seleccionada >= len(pregunta.opciones):
            raise HTTPException(
                status_code=400,
                detail=f"Respuesta debe estar entre 0 y {len(pregunta.opciones) - 1}"
            )
        
        respuesta.respuesta_seleccionada = respuesta_update.respuesta_seleccionada
        respuesta.es_correcta = respuesta_update.respuesta_seleccionada == pregunta.respuesta_correcta
    
    if respuesta_update.tiempo_respuesta_segundos is not None:
        respuesta.tiempo_respuesta_segundos = respuesta_update.tiempo_respuesta_segundos
    
    db.commit()
    db.refresh(respuesta)
    
    return respuesta
