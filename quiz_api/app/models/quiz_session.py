"""
Modelo SQLAlchemy para sesiones de quiz
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class QuizSession(Base):
    """
    Modelo de sesión de quiz.
    
    Campos:
    - id: Identificador único
    - usuario_nombre: Nombre del usuario (opcional)
    - fecha_inicio: Fecha de inicio
    - fecha_fin: Fecha de finalización
    - puntuacion_total: Puntuación total obtenida
    - preguntas_respondidas: Número de preguntas respondidas
    - preguntas_correctas: Número de respuestas correctas
    - estado: Estado de la sesión (en_progreso, completado, abandonado)
    - tiempo_total_segundos: Tiempo total en segundos
    - created_at: Fecha de creación del registro
    """
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_nombre = Column(String(100), nullable=True, index=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)
    puntuacion_total = Column(Integer, default=0)
    preguntas_respondidas = Column(Integer, default=0)
    preguntas_correctas = Column(Integer, default=0)
    estado = Column(String(20), default="en_progreso", index=True)  # en_progreso, completado, abandonado
    tiempo_total_segundos = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relaciones
    answers = relationship("Answer", back_populates="quiz_session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuizSession(id={self.id}, usuario={self.usuario_nombre}, estado={self.estado})>"
