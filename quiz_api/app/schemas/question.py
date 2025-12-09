"""
Schemas Pydantic para preguntas
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class QuestionBase(BaseModel):
    """Schema base para preguntas"""
    pregunta: str = Field(..., min_length=5, max_length=500, description="Texto de la pregunta")
    opciones: List[str] = Field(..., min_items=3, max_items=5, description="Lista de opciones (3-5)")
    respuesta_correcta: int = Field(..., ge=0, description="Índice de la respuesta correcta")
    explicacion: Optional[str] = Field(None, max_length=1000, description="Explicación opcional")
    categoria: str = Field(..., min_length=2, max_length=50, description="Categoría de la pregunta")
    dificultad: str = Field(..., description="Nivel de dificultad: fácil, medio, difícil")

    @field_validator("respuesta_correcta")
    @classmethod
    def validar_respuesta_correcta(cls, v, info):
        """Valida que respuesta_correcta esté dentro del rango de opciones"""
        if "opciones" in info.data:
            opciones_count = len(info.data["opciones"])
            if v >= opciones_count or v < 0:
                raise ValueError(f"respuesta_correcta debe estar entre 0 y {opciones_count - 1}")
        return v

    @field_validator("dificultad")
    @classmethod
    def validar_dificultad(cls, v):
        """Valida que dificultad sea uno de los valores permitidos"""
        valores_validos = ["fácil", "medio", "difícil"]
        if v.lower() not in valores_validos:
            raise ValueError(f"dificultad debe ser una de: {valores_validos}")
        return v.lower()


class QuestionCreate(QuestionBase):
    """Schema para crear preguntas"""
    pass


class QuestionUpdate(BaseModel):
    """Schema para actualizar preguntas"""
    pregunta: Optional[str] = Field(None, min_length=5, max_length=500)
    opciones: Optional[List[str]] = Field(None, min_items=3, max_items=5)
    respuesta_correcta: Optional[int] = Field(None, ge=0)
    explicacion: Optional[str] = Field(None, max_length=1000)
    categoria: Optional[str] = Field(None, min_length=2, max_length=50)
    dificultad: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("dificultad")
    @classmethod
    def validar_dificultad(cls, v):
        """Valida que dificultad sea uno de los valores permitidos"""
        if v is not None:
            valores_validos = ["fácil", "medio", "difícil"]
            if v.lower() not in valores_validos:
                raise ValueError(f"dificultad debe ser una de: {valores_validos}")
            return v.lower()
        return v


class QuestionResponse(QuestionBase):
    """Schema para respuestas de preguntas"""
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class QuestionBulkCreate(BaseModel):
    """Schema para crear múltiples preguntas"""
    preguntas: List[QuestionCreate] = Field(..., min_items=1, description="Lista de preguntas a crear")
