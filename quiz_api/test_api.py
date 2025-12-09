"""
Script para probar todos los endpoints de la API
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

# Colores para la salida
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_test(name):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}TEST: {name}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")


def print_info(msg):
    print(f"{Colors.YELLOW}ℹ {msg}{Colors.RESET}")


def print_response(response):
    print(f"\nStatus Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_health():
    """Probar endpoint de health check"""
    print_test("Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print_success("API está disponible")
        print_response(response)
    else:
        print_error("Health check falló")
        print_response(response)


def test_root():
    """Probar endpoint raíz"""
    print_test("Root Endpoint")
    
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print_success("Endpoint raíz funcionando")
        print_response(response)
    else:
        print_error("Root endpoint falló")
        print_response(response)


def test_get_questions():
    """Probar obtener preguntas"""
    print_test("GET /questions/ - Listar preguntas")
    
    response = requests.get(f"{BASE_URL}/questions/?skip=0&limit=3")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Obtenidas {len(data)} preguntas")
        print_response(response)
        return data[0]['id'] if data else None
    else:
        print_error("No se pudieron obtener preguntas")
        print_response(response)
    return None


def test_get_question_by_id(question_id):
    """Probar obtener pregunta por ID"""
    print_test(f"GET /questions/{question_id} - Obtener pregunta por ID")
    
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        print_success("Pregunta obtenida")
        print_response(response)
    else:
        print_error("No se pudo obtener la pregunta")
        print_response(response)


def test_random_questions():
    """Probar obtener preguntas aleatorias"""
    print_test("GET /questions/random - Obtener preguntas aleatorias")
    
    response = requests.get(f"{BASE_URL}/questions/random?limit=3&categoria=Tecnología")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Obtenidas {len(data)} preguntas aleatorias")
        print_response(response)
        return data
    else:
        print_error("No se pudieron obtener preguntas aleatorias")
        print_response(response)
    return []


def test_create_session():
    """Probar crear sesión de quiz"""
    print_test("POST /quiz-sessions/ - Crear sesión")
    
    payload = {"usuario_nombre": "Test User"}
    response = requests.post(f"{BASE_URL}/quiz-sessions/", json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success("Sesión creada")
        print_response(response)
        return data['id']
    else:
        print_error("No se pudo crear la sesión")
        print_response(response)
    return None


def test_get_sessions():
    """Probar obtener sesiones"""
    print_test("GET /quiz-sessions/ - Listar sesiones")
    
    response = requests.get(f"{BASE_URL}/quiz-sessions/?skip=0&limit=5")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Obtenidas {len(data)} sesiones")
        print_response(response)
    else:
        print_error("No se pudieron obtener sesiones")
        print_response(response)


def test_create_answer(session_id, question_id, respuesta_seleccionada=0):
    """Probar registrar respuesta"""
    print_test(f"POST /answers/ - Registrar respuesta")
    
    payload = {
        "quiz_session_id": session_id,
        "question_id": question_id,
        "respuesta_seleccionada": respuesta_seleccionada,
        "tiempo_respuesta_segundos": 15
    }
    response = requests.post(f"{BASE_URL}/answers/", json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success("Respuesta registrada")
        print_info(f"Correcta: {data['es_correcta']}")
        print_response(response)
        return data['id']
    else:
        print_error("No se pudo registrar la respuesta")
        print_response(response)
    return None


def test_get_answers_session(session_id):
    """Probar obtener respuestas de sesión"""
    print_test(f"GET /answers/session/{session_id} - Obtener respuestas de sesión")
    
    response = requests.get(f"{BASE_URL}/answers/session/{session_id}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Obtenidas {len(data)} respuestas")
        print_response(response)
    else:
        print_error("No se pudieron obtener respuestas")
        print_response(response)


def test_complete_session(session_id):
    """Probar completar sesión"""
    print_test(f"PUT /quiz-sessions/{session_id}/complete - Completar sesión")
    
    payload = {"tiempo_total_segundos": 300}
    response = requests.put(f"{BASE_URL}/quiz-sessions/{session_id}/complete", json=payload)
    if response.status_code == 200:
        data = response.json()
        print_success("Sesión completada")
        print_info(f"Puntuación: {data['puntuacion_total']}")
        print_info(f"Aciertos: {data['preguntas_correctas']}/{data['preguntas_respondidas']}")
        print_response(response)
    else:
        print_error("No se pudo completar la sesión")
        print_response(response)


def test_statistics_global():
    """Probar estadísticas globales"""
    print_test("GET /statistics/global - Estadísticas globales")
    
    response = requests.get(f"{BASE_URL}/statistics/global")
    if response.status_code == 200:
        print_success("Estadísticas obtenidas")
        print_response(response)
    else:
        print_error("No se pudieron obtener estadísticas")
        print_response(response)


def test_statistics_session(session_id):
    """Probar estadísticas de sesión"""
    print_test(f"GET /statistics/session/{session_id} - Estadísticas de sesión")
    
    response = requests.get(f"{BASE_URL}/statistics/session/{session_id}")
    if response.status_code == 200:
        print_success("Estadísticas de sesión obtenidas")
        print_response(response)
    else:
        print_error("No se pudieron obtener estadísticas")
        print_response(response)


def test_statistics_difficult():
    """Probar preguntas difíciles"""
    print_test("GET /statistics/questions/difficult - Preguntas con mayor tasa de error")
    
    response = requests.get(f"{BASE_URL}/statistics/questions/difficult?limit=5")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Obtenidas {len(data)} preguntas difíciles")
        print_response(response)
    else:
        print_error("No se pudieron obtener preguntas difíciles")
        print_response(response)


def test_statistics_categories():
    """Probar rendimiento por categoría"""
    print_test("GET /statistics/categories - Rendimiento por categoría")
    
    response = requests.get(f"{BASE_URL}/statistics/categories")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Obtenidos datos de {len(data)} categorías")
        print_response(response)
    else:
        print_error("No se pudieron obtener estadísticas por categoría")
        print_response(response)


def main():
    """Ejecutar todos los tests"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}PRUEBAS DE API - QUIZ INTERACTIVO{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.RESET}")
    
    # Test basic endpoints
    test_health()
    sleep(0.5)
    test_root()
    sleep(0.5)
    
    # Test questions
    test_get_questions()
    sleep(0.5)
    
    # Test random questions
    preguntas_random = test_random_questions()
    sleep(0.5)
    
    if preguntas_random:
        test_get_question_by_id(preguntas_random[0]['id'])
        sleep(0.5)
    
    # Test sessions
    test_get_sessions()
    sleep(0.5)
    
    session_id = test_create_session()
    sleep(0.5)
    
    if session_id and preguntas_random:
        # Test answers
        for i, pregunta in enumerate(preguntas_random[:3]):
            answer_id = test_create_answer(session_id, pregunta['id'], 0)
            sleep(0.5)
        
        test_get_answers_session(session_id)
        sleep(0.5)
        
        # Complete session
        test_complete_session(session_id)
        sleep(0.5)
        
        # Test statistics
        test_statistics_session(session_id)
        sleep(0.5)
    
    # Global statistics
    test_statistics_global()
    sleep(0.5)
    
    test_statistics_difficult()
    sleep(0.5)
    
    test_statistics_categories()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}✓ TODAS LAS PRUEBAS COMPLETADAS{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.RESET}\n")


if __name__ == "__main__":
    main()
