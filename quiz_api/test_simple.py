"""
Script simple para probar los endpoints principales
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*60)
print("PRUEBAS DE API - QUIZ INTERACTIVO")
print("="*60)

# 1. Test health
print("\n1. Test Health Check")
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   Error: {e}")

# 2. Get all questions
print("\n2. GET /questions/")
try:
    r = requests.get(f"{BASE_URL}/questions/?limit=2", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Preguntas obtenidas: {len(data)}")
    if data:
        print(f"   Primera pregunta: {data[0]['pregunta'][:40]}...")
        question_id = data[0]['id']
except Exception as e:
    print(f"   Error: {e}")

# 3. Get random questions
print("\n3. GET /questions/random")
try:
    r = requests.get(f"{BASE_URL}/questions/random?limit=3", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Preguntas aleatorias obtenidas: {len(data)}")
except Exception as e:
    print(f"   Error: {e}")

# 4. Create quiz session
print("\n4. POST /quiz-sessions/")
try:
    payload = {"usuario_nombre": "Test User"}
    r = requests.post(f"{BASE_URL}/quiz-sessions/", json=payload, timeout=5)
    print(f"   Status: {r.status_code}")
    session = r.json()
    session_id = session['id']
    print(f"   Sesión creada con ID: {session_id}")
    print(f"   Estado: {session['estado']}")
except Exception as e:
    print(f"   Error: {e}")

# 5. Get sessions
print("\n5. GET /quiz-sessions/")
try:
    r = requests.get(f"{BASE_URL}/quiz-sessions/?limit=3", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Sesiones obtenidas: {len(data)}")
except Exception as e:
    print(f"   Error: {e}")

# 6. Register answer
print("\n6. POST /answers/")
try:
    payload = {
        "quiz_session_id": session_id,
        "question_id": question_id,
        "respuesta_seleccionada": 0,
        "tiempo_respuesta_segundos": 15
    }
    r = requests.post(f"{BASE_URL}/answers/", json=payload, timeout=5)
    print(f"   Status: {r.status_code}")
    answer = r.json()
    print(f"   Respuesta registrada")
    print(f"   Correcta: {answer['es_correcta']}")
except Exception as e:
    print(f"   Error: {e}")

# 7. Get session answers
print("\n7. GET /answers/session/{session_id}")
try:
    r = requests.get(f"{BASE_URL}/answers/session/{session_id}", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Respuestas de la sesión: {len(data)}")
except Exception as e:
    print(f"   Error: {e}")

# 8. Complete session
print("\n8. PUT /quiz-sessions/{session_id}/complete")
try:
    payload = {"tiempo_total_segundos": 300}
    r = requests.put(f"{BASE_URL}/quiz-sessions/{session_id}/complete", json=payload, timeout=5)
    print(f"   Status: {r.status_code}")
    session = r.json()
    print(f"   Sesión completada")
    print(f"   Puntuación: {session['puntuacion_total']}")
    print(f"   Aciertos: {session['preguntas_correctas']}/{session['preguntas_respondidas']}")
except Exception as e:
    print(f"   Error: {e}")

# 9. Get statistics global
print("\n9. GET /statistics/global")
try:
    r = requests.get(f"{BASE_URL}/statistics/global", timeout=5)
    print(f"   Status: {r.status_code}")
    stats = r.json()
    print(f"   Total preguntas activas: {stats['total_preguntas_activas']}")
    print(f"   Total sesiones completadas: {stats['total_sesiones_completadas']}")
    print(f"   Promedio aciertos: {stats['promedio_aciertos_general']:.2f}%")
except Exception as e:
    print(f"   Error: {e}")

# 10. Get statistics by session
print("\n10. GET /statistics/session/{session_id}")
try:
    r = requests.get(f"{BASE_URL}/statistics/session/{session_id}", timeout=5)
    print(f"   Status: {r.status_code}")
    stats = r.json()
    print(f"   Puntuación total: {stats['puntuacion_total']}")
    print(f"   Porcentaje aciertos: {stats['porcentaje_aciertos']:.2f}%")
except Exception as e:
    print(f"   Error: {e}")

# 11. Get difficult questions
print("\n11. GET /statistics/questions/difficult")
try:
    r = requests.get(f"{BASE_URL}/statistics/questions/difficult?limit=5", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Preguntas difíciles encontradas: {len(data)}")
except Exception as e:
    print(f"   Error: {e}")

# 12. Get statistics by category
print("\n12. GET /statistics/categories")
try:
    r = requests.get(f"{BASE_URL}/statistics/categories", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(f"   Categorías encontradas: {len(data)}")
    if data:
        for cat in data:
            print(f"     - {cat['categoria']}: {cat['porcentaje_aciertos']:.2f}% aciertos")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*60)
print("✓ TODAS LAS PRUEBAS COMPLETADAS")
print("="*60 + "\n")
