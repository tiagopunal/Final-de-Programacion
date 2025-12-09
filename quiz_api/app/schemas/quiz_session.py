"""
Schemas Pydantic para sesiones de quiz
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuizSessionBase(BaseModel):
    """Schema base para sesiones de quiz"""
    usuario_nombre: Optional[str] = Field(None, max_length=100, description="Nombre del usuario")


class QuizSessionCreate(QuizSessionBase):
    """Schema para crear sesiones de quiz"""
    pass


class QuizSessionUpdate(BaseModel):
    """Schema para actualizar sesiones de quiz"""
    usuario_nombre: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = None
    tiempo_total_segundos: Optional[int] = Field(None, ge=0)


class QuizSessionResponse(QuizSessionBase):
    """Schema para respuestas de sesiones de quiz"""
    id: int
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    puntuacion_total: int
    preguntas_respondidas: int
    preguntas_correctas: int
    estado: str
    tiempo_total_segundos: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class QuizSessionComplete(BaseModel):
    """Schema para completar una sesión de quiz"""
    tiempo_total_segundos: Optional[int] = Field(None, ge=0, description="Tiempo total en segundos")
