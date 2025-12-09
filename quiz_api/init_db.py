"""
Script para inicializar la base de datos con datos de prueba.
Ejecutar con: python init_db.py
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Agregar el directorio raíz al path
sys.path.insert(0, '.')

from app.database import SessionLocal, init_db
from app.models.question import Question
from app.models.quiz_session import QuizSession
from app.models.answer import Answer


def crear_preguntas(db: Session):
    """Crea 15+ preguntas de prueba en diferentes categorías"""
    
    preguntas_data = [
        # Tecnología (5 preguntas)
        {
            "pregunta": "¿Qué es FastAPI?",
            "opciones": ["Una base de datos", "Un framework web", "Un lenguaje de programación", "Un editor"],
            "respuesta_correcta": 1,
            "explicacion": "FastAPI es un framework web moderno y rápido para construir APIs con Python",
            "categoria": "Tecnología",
            "dificultad": "fácil"
        },
        {
            "pregunta": "¿Qué es SQLAlchemy?",
            "opciones": ["Un lenguaje", "Un ORM para Python", "Una base de datos", "Un servidor web"],
            "respuesta_correcta": 1,
            "explicacion": "SQLAlchemy es un ORM (Object-Relational Mapping) muy popular para Python",
            "categoria": "Tecnología",
            "dificultad": "medio"
        },
        {
            "pregunta": "¿Cuál es el propósito principal de una API REST?",
            "opciones": ["Almacenar datos", "Proporcionar interfaces para comunicación entre aplicaciones", "Compilar código", "Crear interfaces gráficas"],
            "respuesta_correcta": 1,
            "explicacion": "Una API REST permite que diferentes aplicaciones se comuniquen entre sí a través de HTTP",
            "categoria": "Tecnología",
            "dificultad": "medio"
        },
        {
            "pregunta": "¿Qué significa CRUD?",
            "opciones": ["Create, Read, Update, Destroy", "Create, Read, Update, Delete", "Compile, Run, Update, Debug", "Create, Request, Use, Display"],
            "respuesta_correcta": 1,
            "explicacion": "CRUD son las operaciones básicas: Create (Crear), Read (Leer), Update (Actualizar), Delete (Borrar)",
            "categoria": "Tecnología",
            "dificultad": "fácil"
        },
        {
            "pregunta": "¿Cuál es la función de Pydantic?",
            "opciones": ["Gestionar archivos", "Validar datos", "Crear servidores", "Compilar código"],
            "respuesta_correcta": 1,
            "explicacion": "Pydantic es una librería para validación y parseo de datos en Python",
            "categoria": "Tecnología",
            "dificultad": "medio"
        },
        
        # Ciencia (5 preguntas)
        {
            "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
            "opciones": ["Tierra", "Marte", "Júpiter", "Saturno"],
            "respuesta_correcta": 2,
            "explicacion": "Júpiter es el planeta más grande del sistema solar con un diámetro de 139,820 km",
            "categoria": "Ciencia",
            "dificultad": "fácil"
        },
        {
            "pregunta": "¿Cuál es la velocidad de la luz?",
            "opciones": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "100,000 km/s"],
            "respuesta_correcta": 0,
            "explicacion": "La velocidad de la luz es aproximadamente 299,792 km/s, o 300,000 km/s",
            "categoria": "Ciencia",
            "dificultad": "medio"
        },
        {
            "pregunta": "¿Cuántos elementos hay en la tabla periódica actualmente?",
            "opciones": ["92", "100", "118", "150"],
            "respuesta_correcta": 2,
            "explicacion": "La tabla periódica moderna contiene 118 elementos químicos confirmados",
            "categoria": "Ciencia",
            "dificultad": "difícil"
        },
        {
            "pregunta": "¿Cuál es el órgano más grande del cuerpo humano?",
            "opciones": ["Corazón", "Cerebro", "Hígado", "Piel"],
            "respuesta_correcta": 3,
            "explicacion": "La piel es el órgano más grande del cuerpo humano, con un área aproximada de 2 metros cuadrados",
            "categoria": "Ciencia",
            "dificultad": "fácil"
        },
        {
            "pregunta": "¿Cuál es la unidad básica de la vida?",
            "opciones": ["Átomo", "Molécula", "Célula", "Gen"],
            "respuesta_correcta": 2,
            "explicacion": "La célula es la unidad básica de la vida y el componente fundamental de todos los organismos vivos",
            "categoria": "Ciencia",
            "dificultad": "fácil"
        },
        
        # Historia (5 preguntas)
        {
            "pregunta": "¿En qué año comenzó la Primera Guerra Mundial?",
            "opciones": ["1912", "1914", "1916", "1918"],
            "respuesta_correcta": 1,
            "explicacion": "La Primera Guerra Mundial comenzó el 28 de julio de 1914 con la declaración de guerra de Austria a Serbia",
            "categoria": "Historia",
            "dificultad": "medio"
        },
        {
            "pregunta": "¿Cuál fue el primer presidente de los Estados Unidos?",
            "opciones": ["Thomas Jefferson", "George Washington", "John Adams", "James Madison"],
            "respuesta_correcta": 1,
            "explicacion": "George Washington fue el primer presidente de los Estados Unidos (1789-1797)",
            "categoria": "Historia",
            "dificultad": "fácil"
        },
        {
            "pregunta": "¿En qué año terminó la Segunda Guerra Mundial?",
            "opciones": ["1943", "1944", "1945", "1946"],
            "respuesta_correcta": 2,
            "explicacion": "La Segunda Guerra Mundial terminó el 2 de septiembre de 1945",
            "categoria": "Historia",
            "dificultad": "medio"
        },
        {
            "pregunta": "¿Cuál fue el imperio más grande de la historia?",
            "opciones": ["Imperio Romano", "Imperio Mongol", "Imperio Británico", "Imperio Español"],
            "respuesta_correcta": 2,
            "explicacion": "El Imperio Británico fue el más grande territorialmente en su apogeo (siglo XIX)",
            "categoria": "Historia",
            "dificultad": "difícil"
        },
        {
            "pregunta": "¿En qué año llegó Cristóbal Colón a América?",
            "opciones": ["1490", "1491", "1492", "1493"],
            "respuesta_correcta": 2,
            "explicacion": "Cristóbal Colón llegó a América el 12 de octubre de 1492",
            "categoria": "Historia",
            "dificultad": "fácil"
        },
    ]
    
    preguntas_creadas = []
    for pregunta_data in preguntas_data:
        pregunta = Question(**pregunta_data)
        db.add(pregunta)
        preguntas_creadas.append(pregunta)
    
    db.commit()
    
    # Refrescar para obtener IDs
    for pregunta in preguntas_creadas:
        db.refresh(pregunta)
    
    print(f"✓ {len(preguntas_creadas)} preguntas creadas")
    return preguntas_creadas


def crear_sesiones_y_respuestas(db: Session, preguntas: list):
    """Crea 3 sesiones de quiz completadas con respuestas"""
    
    usuarios = ["Juan Pérez", "María García", "Carlos López"]
    sesiones_creadas = []
    
    for usuario_nombre in usuarios:
        # Crear sesión
        sesion = QuizSession(
            usuario_nombre=usuario_nombre,
            estado="completado",
            fecha_inicio=datetime.utcnow() - timedelta(days=5),
            fecha_fin=datetime.utcnow() - timedelta(days=4)
        )
        db.add(sesion)
        db.flush()  # Obtener el ID sin hacer commit
        
        # Crear respuestas aleatorias para esta sesión
        import random
        
        # Seleccionar 8 preguntas aleatorias
        preguntas_seleccionadas = random.sample(preguntas, min(8, len(preguntas)))
        
        respuestas_correctas = 0
        tiempo_total = 0
        
        for i, pregunta in enumerate(preguntas_seleccionadas):
            # Generar una respuesta correcta o incorrecta aleatoriamente
            es_correcta_prob = random.random()
            
            if es_correcta_prob > 0.3:  # 70% de probabilidad de acertar
                respuesta_seleccionada = pregunta.respuesta_correcta
                es_correcta = True
                respuestas_correctas += 1
            else:
                # Seleccionar una respuesta incorrecta
                opciones_incorrectas = [i for i in range(len(pregunta.opciones)) if i != pregunta.respuesta_correcta]
                respuesta_seleccionada = random.choice(opciones_incorrectas)
                es_correcta = False
            
            tiempo_respuesta = random.randint(5, 60)
            tiempo_total += tiempo_respuesta
            
            respuesta = Answer(
                quiz_session_id=sesion.id,
                question_id=pregunta.id,
                respuesta_seleccionada=respuesta_seleccionada,
                es_correcta=es_correcta,
                tiempo_respuesta_segundos=tiempo_respuesta
            )
            db.add(respuesta)
        
        # Actualizar estadísticas de la sesión
        sesion.preguntas_respondidas = len(preguntas_seleccionadas)
        sesion.preguntas_correctas = respuestas_correctas
        sesion.puntuacion_total = respuestas_correctas * 10
        sesion.tiempo_total_segundos = tiempo_total
        
        sesiones_creadas.append(sesion)
    
    db.commit()
    
    print(f"✓ {len(sesiones_creadas)} sesiones de quiz creadas con respuestas")
    return sesiones_creadas


def main():
    """Función principal para inicializar la base de datos"""
    
    print("🚀 Inicializando base de datos...")
    
    # Crear tablas
    init_db()
    print("✓ Tablas creadas")
    
    # Obtener sesión
    db = SessionLocal()
    
    try:
        # Crear preguntas
        preguntas = crear_preguntas(db)
        
        # Crear sesiones y respuestas
        sesiones = crear_sesiones_y_respuestas(db, preguntas)
        
        print("\n✅ Base de datos inicializada correctamente")
        print(f"   - Preguntas: {len(preguntas)}")
        print(f"   - Sesiones: {len(sesiones)}")
        
    except Exception as e:
        print(f"❌ Error al inicializar: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
