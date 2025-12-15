# Quiz API (breve)

Pequeña API REST para gestionar un quiz (FastAPI + SQLAlchemy + SQLite).

Nota: la base de datos pre-poblada `quiz_api.db` ya está incluida en el repositorio; no es necesario ejecutar `init_db.py` si no deseas regenerar los datos.

para arrancar y probar:

1) Instalar dependencias

```powershell
pip install -r requirements.txt
```

2) Iniciar el servidor (desde la carpeta del proyecto)

```powershell
uvicorn app.main:app --reload --port 8001
```

3) Abrir en el navegador

- Frontend simple: http://127.0.0.1:8001
- Swagger UI (probar endpoints): http://127.0.0.1:8001/docs
- ReDoc (documentación): http://127.0.0.1:8001/redoc

Endpoints principales (resumen):
- POST /questions/        Crear pregunta
- GET  /questions/        Listar preguntas
- DELETE /questions/{id}  Eliminar pregunta (soft-delete)
- POST /quiz-sessions/    Iniciar sesión de quiz
- POST /answers/          Registrar respuesta

Nota rápida:
- `respuesta_correcta` es un índice (0-based) que apunta a la opción correcta en `opciones`.
- El DELETE sobre `/questions/{id}` hace soft-delete (la pregunta se marca inactiva).

Ejemplo mínimo para crear una pregunta (JSON):

```json
{
  "pregunta": "¿Cuál es la capital de Francia?",
  "opciones": ["Madrid", "París", "Roma", "Berlín"],
  "respuesta_correcta": 1,
  "explicacion": "París es la capital de Francia",
  "categoria": "Geografía",
  "dificultad": "fácil"
}

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

## Ejecutar localmente (Windows - PowerShell)

Pasos mínimos para que tu profesor pueda ejecutar y probar el proyecto en Windows:

1. Abrir PowerShell y ubicarse en la carpeta `quiz_api` del proyecto.

2. Crear y activar un virtualenv (si no existe):

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Copiar variables de entorno y crear datos de prueba (opcional):

```powershell
Copy-Item .env.example .env
# Si quieres crear o refrescar datos de prueba:
python init_db.py
# Nota: el repositorio incluye `quiz_api.db` pre-poblada con preguntas.
```

5. Arrancar el servidor (por defecto usamos el puerto `8001` en este repo):

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
```

6. Abrir en el navegador:

- Frontend: http://127.0.0.1:8001
- Documentación (Swagger UI): http://127.0.0.1:8001/docs

## Crear y ver preguntas

- Desde la UI: abre la página principal y usa el formulario de creación de preguntas. Las preguntas creadas se muestran en la lista.
- Con `curl` (ejemplo POST para crear una pregunta):

```bash
curl -X POST "http://127.0.0.1:8001/questions/" \
  -H "Content-Type: application/json" \
  -d '{
    "pregunta": "¿Cuál es la capital de Francia?",
    "opciones": ["Madrid", "París", "Roma", "Berlín"],
    "respuesta_correcta": 1,
    "explicacion": "París es la capital de Francia",
    "categoria": "Geografía",
    "dificultad": "fácil"
  }'
```

- Listar preguntas (GET):

```bash
curl "http://127.0.0.1:8001/questions/?skip=0&limit=20"
```
## 🧪 Testing

### Crear Datos de Prueba

Se incluye un script para generar datos de prueba. Ejecuta:

```bash
python init_db.py
```

Este script crea:
- 15+ preguntas de diferentes categorías y dificultades
- Respuestas registradas para cada sesión

### Verificar Endpoints

Accede a http://localhost:8000/docs para ver la documentación interactiva y probar todos los endpoints.

## Ejemplos de Respuestas

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

##  Validaciones

La API implementa validaciones en múltiples capas:

- **Pydantic**: Validación de tipos y rangos en inputs
- **Business Logic**: Validaciones de negocio (duplicados, relaciones, etc.)
- **Database**: Constraints a nivel de base de datos

**Ejemplos:**
- Respuesta correcta debe estar en rango de opciones
- No se puede responder la misma pregunta dos veces en una sesión
- Categoría y dificultad deben ser valores válidos

## Códigos de Error

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

##  Notas Importantes

1. **Soft Delete**: Las preguntas se eliminan con soft delete (is_active = False)
2. **Puntuación**: 10 puntos por respuesta correcta
3. **Validación Automática**: Las respuestas se validan automáticamente
4. **Relaciones**: Las respuestas se eliminan en cascada con sesiones y preguntas

---

**¿Preguntas?** Consulta la documentación interactiva en http://localhost:8000/docs
