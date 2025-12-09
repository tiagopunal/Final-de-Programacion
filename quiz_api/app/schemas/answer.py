"""
Schemas Pydantic para respuestas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnswerBase(BaseModel):
    """Schema base para respuestas"""
    quiz_session_id: int = Field(..., gt=0, description="ID de la sesión de quiz")
    question_id: int = Field(..., gt=0, description="ID de la pregunta")
    respuesta_seleccionada: int = Field(..., ge=0, description="Índice de la respuesta seleccionada")
    tiempo_respuesta_segundos: Optional[int] = Field(None, ge=0, description="Tiempo de respuesta en segundos")


class AnswerCreate(AnswerBase):
    """Schema para crear respuestas"""
    pass


class AnswerUpdate(BaseModel):
    """Schema para actualizar respuestas"""
    respuesta_seleccionada: Optional[int] = Field(None, ge=0)
    tiempo_respuesta_segundos: Optional[int] = Field(None, ge=0)


class AnswerResponse(AnswerBase):
    """Schema para respuestas de API"""
    id: int
    es_correcta: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerDetailResponse(AnswerResponse):
    """Schema detallado de respuestas con información de la pregunta"""
    pregunta_texto: Optional[str] = None
    opciones: Optional[list] = None
    respuesta_correcta_indice: Optional[int] = None
    respuesta_seleccionada_texto: Optional[str] = None
