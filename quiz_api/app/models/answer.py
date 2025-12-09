"""
Modelo SQLAlchemy para respuestas de usuarios
"""
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Answer(Base):
    """
    Modelo de respuesta del usuario.
    
    Campos:
    - id: Identificador único
    - quiz_session_id: ID de la sesión de quiz (Foreign Key)
    - question_id: ID de la pregunta (Foreign Key)
    - respuesta_seleccionada: Índice de la respuesta seleccionada
    - es_correcta: Si la respuesta es correcta
    - tiempo_respuesta_segundos: Tiempo que tardó en responder
    - created_at: Fecha de creación del registro
    """
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    respuesta_seleccionada = Column(Integer, nullable=False)
    es_correcta = Column(Boolean, nullable=False)
    tiempo_respuesta_segundos = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relaciones
    quiz_session = relationship("QuizSession", back_populates="answers")
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, session={self.quiz_session_id}, question={self.question_id}, correcta={self.es_correcta})>"
