"""
Servicio de lógica de negocio para quiz
"""
from sqlalchemy.orm import Session
from app.models.question import Question
from app.models.quiz_session import QuizSession
from app.models.answer import Answer
from datetime import datetime
from typing import List, Dict, Any


class QuizService:
    """
    Servicio con la lógica de negocio del quiz.
    Maneja cálculos de puntuaciones, validaciones y estadísticas.
    """

    @staticmethod
    def validar_respuesta(db: Session, question_id: int, respuesta_seleccionada: int) -> bool:
        """
        Valida si una respuesta es correcta.
        
        Args:
            db: Sesión de base de datos
            question_id: ID de la pregunta
            respuesta_seleccionada: Índice de la respuesta seleccionada
            
        Returns:
            bool: True si es correcta, False si no
            
        Raises:
            ValueError: Si la pregunta no existe o la respuesta está fuera de rango
        """
        pregunta = db.query(Question).filter(Question.id == question_id).first()
        if not pregunta:
            raise ValueError(f"La pregunta con ID {question_id} no existe")

        if respuesta_seleccionada < 0 or respuesta_seleccionada >= len(pregunta.opciones):
            raise ValueError(
                f"La respuesta {respuesta_seleccionada} está fuera del rango válido "
                f"(0-{len(pregunta.opciones) - 1})"
            )

        return respuesta_seleccionada == pregunta.respuesta_correcta

    @staticmethod
    def verificar_respuesta_duplicada(db: Session, quiz_session_id: int, question_id: int) -> bool:
        """
        Verifica si el usuario ya respondió esta pregunta en esta sesión.
        
        Args:
            db: Sesión de base de datos
            quiz_session_id: ID de la sesión
            question_id: ID de la pregunta
            
        Returns:
            bool: True si ya existe respuesta, False si no
        """
        respuesta_existente = db.query(Answer).filter(
            Answer.quiz_session_id == quiz_session_id,
            Answer.question_id == question_id
        ).first()
        return respuesta_existente is not None

    @staticmethod
    def calcular_puntuacion_sesion(db: Session, quiz_session_id: int) -> Dict[str, Any]:
        """
        Calcula la puntuación y estadísticas de una sesión de quiz.
        
        Args:
            db: Sesión de base de datos
            quiz_session_id: ID de la sesión
            
        Returns:
            Dict con puntuación, correctas, respondidas, etc.
            
        Raises:
            ValueError: Si la sesión no existe
        """
        sesion = db.query(QuizSession).filter(QuizSession.id == quiz_session_id).first()
        if not sesion:
            raise ValueError(f"La sesión con ID {quiz_session_id} no existe")

        respuestas = db.query(Answer).filter(Answer.quiz_session_id == quiz_session_id).all()
        
        total_respondidas = len(respuestas)
        total_correctas = sum(1 for r in respuestas if r.es_correcta)
        
        # Calcular puntuación: 10 puntos por respuesta correcta
        puntuacion = total_correctas * 10
        
        # Calcular tiempo promedio por respuesta
        tiempos = [r.tiempo_respuesta_segundos for r in respuestas if r.tiempo_respuesta_segundos]
        tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
        
        return {
            "puntuacion_total": puntuacion,
            "preguntas_respondidas": total_respondidas,
            "preguntas_correctas": total_correctas,
            "porcentaje_aciertos": (total_correctas / total_respondidas * 100) if total_respondidas > 0 else 0,
            "tiempo_promedio_por_pregunta": round(tiempo_promedio, 2)
        }

    @staticmethod
    def completar_sesion(db: Session, quiz_session_id: int, tiempo_total_segundos: int = None) -> QuizSession:
        """
        Marca una sesión como completada y calcula su puntuación final.
        
        Args:
            db: Sesión de base de datos
            quiz_session_id: ID de la sesión
            tiempo_total_segundos: Tiempo total opcional
            
        Returns:
            QuizSession actualizada
        """
        sesion = db.query(QuizSession).filter(QuizSession.id == quiz_session_id).first()
        if not sesion:
            raise ValueError(f"La sesión con ID {quiz_session_id} no existe")

        # Calcular puntuación
        estadisticas = QuizService.calcular_puntuacion_sesion(db, quiz_session_id)
        
        # Actualizar sesión
        sesion.puntuacion_total = estadisticas["puntuacion_total"]
        sesion.preguntas_respondidas = estadisticas["preguntas_respondidas"]
        sesion.preguntas_correctas = estadisticas["preguntas_correctas"]
        sesion.estado = "completado"
        sesion.fecha_fin = datetime.utcnow()
        sesion.tiempo_total_segundos = tiempo_total_segundos
        
        db.commit()
        db.refresh(sesion)
        
        return sesion

    @staticmethod
    def obtener_estadisticas_globales(db: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas globales del sistema.
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            Dict con estadísticas globales
        """
        # Total de preguntas activas
        total_preguntas_activas = db.query(Question).filter(Question.is_active == True).count()
        
        # Total de sesiones completadas
        sesiones_completadas = db.query(QuizSession).filter(
            QuizSession.estado == "completado"
        ).all()
        total_sesiones_completadas = len(sesiones_completadas)
        
        # Promedio de aciertos general
        total_respuestas_correctas = 0
        total_respuestas = 0
        for sesion in sesiones_completadas:
            total_respuestas_correctas += sesion.preguntas_correctas
            total_respuestas += sesion.preguntas_respondidas
        
        promedio_aciertos = (total_respuestas_correctas / total_respuestas * 100) if total_respuestas > 0 else 0
        
        # Categorías más difíciles (mayor tasa de error)
        respuestas_por_categoria = db.query(
            Question.categoria,
            Answer.es_correcta
        ).join(
            Answer, Answer.question_id == Question.id
        ).all()
        
        categorias_dificultad = {}
        for categoria, es_correcta in respuestas_por_categoria:
            if categoria not in categorias_dificultad:
                categorias_dificultad[categoria] = {"correctas": 0, "total": 0}
            categorias_dificultad[categoria]["total"] += 1
            if es_correcta:
                categorias_dificultad[categoria]["correctas"] += 1
        
        categorias_ordenadas = sorted(
            [
                {
                    "categoria": cat,
                    "tasa_aciertos": (stats["correctas"] / stats["total"] * 100) if stats["total"] > 0 else 0,
                    "tasa_error": (100 - (stats["correctas"] / stats["total"] * 100)) if stats["total"] > 0 else 0
                }
                for cat, stats in categorias_dificultad.items()
            ],
            key=lambda x: x["tasa_error"],
            reverse=True
        )
        
        return {
            "total_preguntas_activas": total_preguntas_activas,
            "total_sesiones_completadas": total_sesiones_completadas,
            "promedio_aciertos_general": round(promedio_aciertos, 2),
            "categorias_ordenadas_por_dificultad": categorias_ordenadas[:5]  # Top 5
        }

    @staticmethod
    def obtener_preguntas_difíciles(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene las preguntas con mayor tasa de error.
        
        Args:
            db: Sesión de base de datos
            limit: Límite de resultados
            
        Returns:
            Lista de preguntas ordenadas por tasa de error
        """
        respuestas = db.query(
            Answer.question_id,
            Answer.es_correcta
        ).all()
        
        estadisticas_preguntas = {}
        for question_id, es_correcta in respuestas:
            if question_id not in estadisticas_preguntas:
                estadisticas_preguntas[question_id] = {"correctas": 0, "total": 0}
            estadisticas_preguntas[question_id]["total"] += 1
            if es_correcta:
                estadisticas_preguntas[question_id]["correctas"] += 1
        
        # Obtener información de las preguntas
        resultado = []
        for question_id, stats in estadisticas_preguntas.items():
            pregunta = db.query(Question).filter(Question.id == question_id).first()
            if pregunta:
                tasa_error = 100 - (stats["correctas"] / stats["total"] * 100)
                resultado.append({
                    "id": question_id,
                    "pregunta": pregunta.pregunta,
                    "categoria": pregunta.categoria,
                    "dificultad": pregunta.dificultad,
                    "respondidas": stats["total"],
                    "correctas": stats["correctas"],
                    "incorrectas": stats["total"] - stats["correctas"],
                    "tasa_aciertos": round(stats["correctas"] / stats["total"] * 100, 2),
                    "tasa_error": round(tasa_error, 2)
                })
        
        # Ordenar por tasa de error descendente
        resultado.sort(key=lambda x: x["tasa_error"], reverse=True)
        
        return resultado[:limit]

    @staticmethod
    def obtener_rendimiento_por_categoria(db: Session) -> List[Dict[str, Any]]:
        """
        Obtiene el rendimiento promedio por categoría.
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            Lista de categorías con su rendimiento
        """
        categorias = db.query(Question.categoria).distinct().all()
        
        resultado = []
        for (categoria,) in categorias:
            respuestas = db.query(Answer).join(
                Question, Answer.question_id == Question.id
            ).filter(Question.categoria == categoria).all()
            
            if respuestas:
                total = len(respuestas)
                correctas = sum(1 for r in respuestas if r.es_correcta)
                
                resultado.append({
                    "categoria": categoria,
                    "total_preguntas": db.query(Question).filter(
                        Question.categoria == categoria,
                        Question.is_active == True
                    ).count(),
                    "total_respondidas": total,
                    "aciertos": correctas,
                    "errores": total - correctas,
                    "porcentaje_aciertos": round(correctas / total * 100, 2)
                })
        
        return sorted(resultado, key=lambda x: x["porcentaje_aciertos"], reverse=True)
