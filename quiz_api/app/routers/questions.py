"""
Router para gestionar preguntas (CRUD)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import random
from typing import List

from app.database import get_db
from app.models.question import Question
from app.schemas.question import (
    QuestionCreate, QuestionResponse, QuestionUpdate, QuestionBulkCreate
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=QuestionResponse, status_code=201)
def crear_pregunta(
    pregunta: QuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva pregunta.
    
    Args:
        pregunta: Datos de la pregunta a crear
        db: Sesión de base de datos
        
    Returns:
        QuestionResponse: La pregunta creada
    """
    db_pregunta = Question(
        pregunta=pregunta.pregunta,
        opciones=pregunta.opciones,
        respuesta_correcta=pregunta.respuesta_correcta,
        explicacion=pregunta.explicacion,
        categoria=pregunta.categoria,
        dificultad=pregunta.dificultad
    )
    db.add(db_pregunta)
    db.commit()
    db.refresh(db_pregunta)
    return db_pregunta


@router.get("/", response_model=List[QuestionResponse])
def listar_preguntas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    categoria: str = Query(None, description="Filtrar por categoría"),
    dificultad: str = Query(None, description="Filtrar por dificultad (fácil, medio, difícil)"),
    db: Session = Depends(get_db)
):
    """
    Listar preguntas con paginación y filtros opcionales.
    
    Args:
        skip: Número de registros a saltar
        limit: Límite de registros a retornar
        categoria: Filtrar por categoría (opcional)
        dificultad: Filtrar por dificultad (opcional)
        db: Sesión de base de datos
        
    Returns:
        List[QuestionResponse]: Lista de preguntas
    """
    query = db.query(Question).filter(Question.is_active == True)
    
    if categoria:
        query = query.filter(Question.categoria == categoria)
    
    if dificultad:
        query = query.filter(Question.dificultad == dificultad.lower())
    
    preguntas = query.offset(skip).limit(limit).all()
    return preguntas


@router.get("/random", response_model=List[QuestionResponse])
def obtener_preguntas_aleatorias(
    limit: int = Query(10, ge=1, le=50, description="Número de preguntas aleatorias"),
    categoria: str = Query(None, description="Filtrar por categoría"),
    dificultad: str = Query(None, description="Filtrar por dificultad"),
    db: Session = Depends(get_db)
):
    """
    Obtener preguntas aleatorias para un quiz.
    
    Args:
        limit: Número de preguntas aleatorias
        categoria: Filtrar por categoría (opcional)
        dificultad: Filtrar por dificultad (opcional)
        db: Sesión de base de datos
        
    Returns:
        List[QuestionResponse]: Lista de preguntas aleatorias
        
    Raises:
        HTTPException: Si no hay suficientes preguntas disponibles
    """
    query = db.query(Question).filter(Question.is_active == True)
    
    if categoria:
        query = query.filter(Question.categoria == categoria)
    
    if dificultad:
        query = query.filter(Question.dificultad == dificultad.lower())
    
    preguntas = query.all()
    
    if len(preguntas) < limit:
        raise HTTPException(
            status_code=400,
            detail=f"Solo hay {len(preguntas)} preguntas disponibles, se requieren {limit}"
        )
    
    preguntas_seleccionadas = random.sample(preguntas, limit)
    return preguntas_seleccionadas


@router.get("/{question_id}", response_model=QuestionResponse)
def obtener_pregunta(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una pregunta específica por ID.
    
    Args:
        question_id: ID de la pregunta
        db: Sesión de base de datos
        
    Returns:
        QuestionResponse: La pregunta solicitada
        
    Raises:
        HTTPException: Si la pregunta no existe
    """
    pregunta = db.query(Question).filter(Question.id == question_id).first()
    
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    return pregunta


@router.put("/{question_id}", response_model=QuestionResponse)
def actualizar_pregunta(
    question_id: int,
    pregunta_update: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una pregunta existente.
    
    Args:
        question_id: ID de la pregunta
        pregunta_update: Datos a actualizar
        db: Sesión de base de datos
        
    Returns:
        QuestionResponse: La pregunta actualizada
        
    Raises:
        HTTPException: Si la pregunta no existe
    """
    pregunta = db.query(Question).filter(Question.id == question_id).first()
    
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    # Actualizar solo los campos proporcionados
    update_data = pregunta_update.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(pregunta, campo, valor)
    
    db.commit()
    db.refresh(pregunta)
    
    return pregunta


@router.delete("/{question_id}", status_code=204)
def eliminar_pregunta(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una pregunta (soft delete: marcar como inactiva).
    
    Args:
        question_id: ID de la pregunta
        db: Sesión de base de datos
        
    Raises:
        HTTPException: Si la pregunta no existe
    """
    pregunta = db.query(Question).filter(Question.id == question_id).first()
    
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    # Soft delete
    pregunta.is_active = False
    db.commit()


@router.post("/bulk", response_model=List[QuestionResponse], status_code=201)
def crear_preguntas_bulk(
    bulk_data: QuestionBulkCreate,
    db: Session = Depends(get_db)
):
    """
    Crear múltiples preguntas desde JSON.
    
    Args:
        bulk_data: Objeto con lista de preguntas a crear
        db: Sesión de base de datos
        
    Returns:
        List[QuestionResponse]: Lista de preguntas creadas
    """
    preguntas_creadas = []
    
    for pregunta_data in bulk_data.preguntas:
        pregunta = Question(
            pregunta=pregunta_data.pregunta,
            opciones=pregunta_data.opciones,
            respuesta_correcta=pregunta_data.respuesta_correcta,
            explicacion=pregunta_data.explicacion,
            categoria=pregunta_data.categoria,
            dificultad=pregunta_data.dificultad
        )
        db.add(pregunta)
        preguntas_creadas.append(pregunta)
    
    db.commit()
    
    # Refrescar todas las preguntas para obtener los IDs
    for pregunta in preguntas_creadas:
        db.refresh(pregunta)
    
    return preguntas_creadas
