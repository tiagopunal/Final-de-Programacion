"""
Modelo SQLAlchemy para preguntas de quiz
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Question(Base):
    """
    Modelo de pregunta para el quiz.
    
    Campos:
    - id: Identificador único
    - pregunta: Texto de la pregunta
    - opciones: Lista de opciones (JSON)
    - respuesta_correcta: Índice de la respuesta correcta (0-based)
    - explicacion: Explicación opcional de la respuesta
    - categoria: Categoría de la pregunta
    - dificultad: Nivel de dificultad (fácil, medio, difícil)
    - created_at: Fecha de creación
    - is_active: Si la pregunta está activa
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pregunta = Column(String(500), nullable=False, index=True)
    opciones = Column(JSON, nullable=False)  # Array de strings
    respuesta_correcta = Column(Integer, nullable=False)
    explicacion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=False, index=True)
    dificultad = Column(String(20), nullable=False, index=True)  # fácil, medio, difícil
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_active = Column(Boolean, default=True, index=True)

    # Relaciones
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question(id={self.id}, pregunta={self.pregunta[:50]}...)>"
