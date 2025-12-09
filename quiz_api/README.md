# Quiz API REST - FastAPI

Una API REST completa para gestionar un sistema de quiz interactivo, construida con **FastAPI**, **SQLAlchemy** y **SQLite**.

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar servidor
uvicorn app.main:app --port 8000

# 3. Abrir documentación interactiva
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## 📋 Descripción

Esta API proporciona servicios backend para una aplicación de quiz interactivo, incluyendo:

- **Gestión de Preguntas**: CRUD completo, filtrado por categoría y dificultad
- **Sesiones de Quiz**: Iniciar, gestionar y finalizar sesiones de usuarios
- **Registro de Respuestas**: Almacenar y validar respuestas de usuarios
- **Estadísticas**: Reportes globales, por sesión, preguntas difíciles, rendimiento por categoría

## 🚀 Inicio Rápido

### 1. Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalación

**Clonar el repositorio:**

```bash
git clone <tu-repositorio>
cd quiz_api
```

**Crear entorno virtual:**

```bash
# Linux/Mac:
python -m venv venv
source venv/bin/activate

# Windows (PowerShell):
python -m venv venv
venv\Scripts\Activate.ps1

# Windows (CMD):
python -m venv venv
venv\Scripts\activate.bat
```

**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**Configurar variables de entorno (opcional):**

```bash
cp .env.example .env
# Edita .env si necesitas cambiar la configuración
```

### 3. Ejecutar la Aplicación

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: **http://localhost:8000**

### 4. Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Estructura del Proyecto

```
quiz_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Configuración principal de FastAPI
│   ├── database.py             # Configuración de SQLAlchemy
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── question.py         # Modelo de preguntas
│   │   ├── quiz_session.py     # Modelo de sesiones
│   │   └── answer.py           # Modelo de respuestas
│   ├── schemas/                # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── question.py         # Schemas de preguntas
│   │   ├── quiz_session.py     # Schemas de sesiones
│   │   └── answer.py           # Schemas de respuestas
│   ├── routers/                # Rutas de la API
│   │   ├── __init__.py
│   │   ├── questions.py        # Endpoints de preguntas
│   │   ├── quiz_sessions.py    # Endpoints de sesiones
│   │   ├── answers.py          # Endpoints de respuestas
│   │   └── statistics.py       # Endpoints de estadísticas
│   └── services/               # Lógica de negocio
│       ├── __init__.py
│       └── quiz_service.py     # Servicio de quiz
├── requirements.txt            # Dependencias Python
├── .env.example               # Variables de entorno ejemplo
├── .gitignore                 # Archivos a ignorar en Git
└── README.md                  # Este archivo
```

## 🗄️ Modelos de Datos

### Question (Pregunta)

```python
{
  "id": 1,
  "pregunta": "¿Qué es FastAPI?",
  "opciones": ["Una base de datos", "Un framework web", "Un lenguaje", "Un editor"],
  "respuesta_correcta": 1,
  "explicacion": "FastAPI es un framework web moderno y rápido para Python",
  "categoria": "Tecnología",
  "dificultad": "fácil",
  "created_at": "2023-12-09T10:00:00",
  "is_active": true
}
```

### QuizSession (Sesión de Quiz)

```python
{
  "id": 1,
  "usuario_nombre": "Juan Pérez",
  "fecha_inicio": "2023-12-09T10:00:00",
  "fecha_fin": "2023-12-09T10:15:00",
  "puntuacion_total": 80,
  "preguntas_respondidas": 10,
  "preguntas_correctas": 8,
  "estado": "completado",
  "tiempo_total_segundos": 900,
  "created_at": "2023-12-09T10:00:00"
}
```

### Answer (Respuesta)

```python
{
  "id": 1,
  "quiz_session_id": 1,
  "question_id": 1,
  "respuesta_seleccionada": 1,
  "es_correcta": true,
  "tiempo_respuesta_segundos": 15,
  "created_at": "2023-12-09T10:00:30"
}
```

## 🔧 Endpoints de la API

### Preguntas (`/questions`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/questions/` | Crear una nueva pregunta |
| GET | `/questions/` | Listar preguntas con paginación y filtros |
| GET | `/questions/{question_id}` | Obtener pregunta por ID |
| GET | `/questions/random` | Obtener preguntas aleatorias |
| PUT | `/questions/{question_id}` | Actualizar pregunta |
| DELETE | `/questions/{question_id}` | Eliminar pregunta (soft delete) |
| POST | `/questions/bulk` | Crear múltiples preguntas |

**Ejemplo: Crear pregunta**

```bash
curl -X POST "http://localhost:8000/questions/" \
  -H "Content-Type: application/json" \
  -d '{
    "pregunta": "¿Cuál es la capital de Francia?",
    "opciones": ["Madrid", "París", "Londres", "Berlín"],
    "respuesta_correcta": 1,
    "explicacion": "París es la capital de Francia",
    "categoria": "Geografía",
    "dificultad": "fácil"
  }'
```

**Ejemplo: Listar preguntas con filtros**

```bash
curl "http://localhost:8000/questions/?categoria=Tecnología&dificultad=medio&skip=0&limit=10"
```

**Ejemplo: Obtener preguntas aleatorias**

```bash
curl "http://localhost:8000/questions/random?limit=5&categoria=Ciencia"
```

### Sesiones de Quiz (`/quiz-sessions`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/quiz-sessions/` | Iniciar nueva sesión |
| GET | `/quiz-sessions/` | Listar sesiones |
| GET | `/quiz-sessions/{session_id}` | Obtener sesión por ID |
| PUT | `/quiz-sessions/{session_id}/complete` | Finalizar sesión |
| DELETE | `/quiz-sessions/{session_id}` | Eliminar sesión |

**Ejemplo: Iniciar sesión**

```bash
curl -X POST "http://localhost:8000/quiz-sessions/" \
  -H "Content-Type: application/json" \
  -d '{"usuario_nombre": "Juan Pérez"}'
```

**Ejemplo: Finalizar sesión**

```bash
curl -X PUT "http://localhost:8000/quiz-sessions/1/complete" \
  -H "Content-Type: application/json" \
  -d '{"tiempo_total_segundos": 900}'
```

### Respuestas (`/answers`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/answers/` | Registrar respuesta |
| GET | `/answers/session/{session_id}` | Obtener respuestas de sesión |
| GET | `/answers/{answer_id}` | Obtener respuesta por ID |
| PUT | `/answers/{answer_id}` | Actualizar respuesta |

**Ejemplo: Registrar respuesta**

```bash
curl -X POST "http://localhost:8000/answers/" \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_session_id": 1,
    "question_id": 1,
    "respuesta_seleccionada": 1,
    "tiempo_respuesta_segundos": 15
  }'
```

**Ejemplo: Obtener respuestas de una sesión**

```bash
curl "http://localhost:8000/answers/session/1"
```

### Estadísticas (`/statistics`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/statistics/global` | Estadísticas globales del sistema |
| GET | `/statistics/session/{session_id}` | Estadísticas de una sesión |
| GET | `/statistics/questions/difficult` | Preguntas con mayor tasa de error |
| GET | `/statistics/categories` | Rendimiento por categoría |

**Ejemplo: Obtener estadísticas globales**

```bash
curl "http://localhost:8000/statistics/global"
```

**Ejemplo: Obtener estadísticas de sesión**

```bash
curl "http://localhost:8000/statistics/session/1"
```

**Ejemplo: Obtener preguntas difíciles**

```bash
curl "http://localhost:8000/statistics/questions/difficult?limit=10"
```

**Ejemplo: Obtener rendimiento por categoría**

```bash
curl "http://localhost:8000/statistics/categories"
```

## 💡 Flujo de Uso

### 1. Crear Preguntas

```bash
# Crear una o más preguntas
curl -X POST "http://localhost:8000/questions/" \
  -H "Content-Type: application/json" \
  -d '...'
```

### 2. Iniciar Sesión de Quiz

```bash
# Crear nueva sesión
curl -X POST "http://localhost:8000/quiz-sessions/" \
  -H "Content-Type: application/json" \
  -d '{"usuario_nombre": "Usuario"}'
# Respuesta: {"id": 1, "estado": "en_progreso", ...}
```

### 3. Obtener Preguntas para el Quiz

```bash
# Obtener preguntas aleatorias
curl "http://localhost:8000/questions/random?limit=10"
```

### 4. Registrar Respuestas

```bash
# Por cada pregunta respondida
curl -X POST "http://localhost:8000/answers/" \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_session_id": 1,
    "question_id": 1,
    "respuesta_seleccionada": 1,
    "tiempo_respuesta_segundos": 15
  }'
```

### 5. Finalizar Quiz

```bash
# Completar la sesión
curl -X PUT "http://localhost:8000/quiz-sessions/1/complete" \
  -H "Content-Type: application/json" \
  -d '{"tiempo_total_segundos": 300}'
```

### 6. Obtener Resultados

```bash
# Ver estadísticas de la sesión
curl "http://localhost:8000/statistics/session/1"
```

## 🧪 Testing

### Crear Datos de Prueba

Se incluye un script para generar datos de prueba. Ejecuta:

```bash
python init_db.py
```

Este script crea:
- 15+ preguntas de diferentes categorías y dificultades
- 3+ sesiones de quiz completadas
- Respuestas registradas para cada sesión

### Verificar Endpoints

Accede a http://localhost:8000/docs para ver la documentación interactiva y probar todos los endpoints.

## 📊 Ejemplos de Respuestas

### Crear Pregunta (POST /questions/)

**Request:**
```json
{
  "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
  "opciones": ["Tierra", "Marte", "Júpiter", "Saturno"],
  "respuesta_correcta": 2,
  "explicacion": "Júpiter es el planeta más grande del sistema solar",
  "categoria": "Astronomía",
  "dificultad": "medio"
}
```

**Response:**
```json
{
  "id": 1,
  "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
  "opciones": ["Tierra", "Marte", "Júpiter", "Saturno"],
  "respuesta_correcta": 2,
  "explicacion": "Júpiter es el planeta más grande del sistema solar",
  "categoria": "Astronomía",
  "dificultad": "medio",
  "created_at": "2023-12-09T10:00:00",
  "is_active": true
}
```

### Registrar Respuesta (POST /answers/)

**Request:**
```json
{
  "quiz_session_id": 1,
  "question_id": 1,
  "respuesta_seleccionada": 2,
  "tiempo_respuesta_segundos": 20
}
```

**Response:**
```json
{
  "id": 1,
  "quiz_session_id": 1,
  "question_id": 1,
  "respuesta_seleccionada": 2,
  "es_correcta": true,
  "tiempo_respuesta_segundos": 20,
  "created_at": "2023-12-09T10:00:30"
}
```

### Estadísticas de Sesión (GET /statistics/session/{session_id})

```json
{
  "id_sesion": 1,
  "usuario_nombre": "Juan Pérez",
  "fecha_inicio": "2023-12-09T10:00:00",
  "fecha_fin": "2023-12-09T10:15:00",
  "estado": "completado",
  "puntuacion_total": 80,
  "preguntas_respondidas": 10,
  "preguntas_correctas": 8,
  "porcentaje_aciertos": 80.0,
  "tiempo_total_segundos": 900,
  "tiempo_promedio_por_pregunta": 90.0
}
```

## 🔒 Validaciones

La API implementa validaciones en múltiples capas:

- **Pydantic**: Validación de tipos y rangos en inputs
- **Business Logic**: Validaciones de negocio (duplicados, relaciones, etc.)
- **Database**: Constraints a nivel de base de datos

**Ejemplos:**
- Respuesta correcta debe estar en rango de opciones
- No se puede responder la misma pregunta dos veces en una sesión
- Categoría y dificultad deben ser valores válidos

## 🚨 Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Eliminación exitosa |
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Server Error - Error del servidor |

## 📁 Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Conexión a base de datos
DATABASE_URL=sqlite:///./quiz_api.db

# Modo debug
DEBUG=True
```

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno para APIs
- **SQLAlchemy**: ORM para Python
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## 📝 Notas Importantes

1. **Soft Delete**: Las preguntas se eliminan con soft delete (is_active = False)
2. **Puntuación**: 10 puntos por respuesta correcta
3. **Validación Automática**: Las respuestas se validan automáticamente
4. **Relaciones**: Las respuestas se eliminan en cascada con sesiones y preguntas

## 🤝 Contribuciones

Este proyecto es un examen final. Para cambios significativos, por favor abre un issue primero.

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 👤 Autor

Desarrollado como examen final del curso de Programación.

---

**¿Preguntas?** Consulta la documentación interactiva en http://localhost:8000/docs
