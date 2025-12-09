#!/usr/bin/env python3
"""
VERIFICACIÓN FINAL DEL PROYECTO
Ejecutar: python verify_project.py
Verifica que todos los archivos y componentes están presentes y funcionales.
"""

import os
import sys
from pathlib import Path

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def check_file(path, description=""):
    """Verifica si un archivo existe"""
    exists = os.path.exists(path)
    symbol = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    desc = f" - {description}" if description else ""
    print(f"  {symbol} {Path(path).name}{desc}")
    return exists

def check_directory(path, description=""):
    """Verifica si un directorio existe"""
    exists = os.path.isdir(path)
    symbol = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    desc = f" - {description}" if description else ""
    print(f"  {symbol} {Path(path).name}/{desc}")
    return exists

def main():
    os.chdir("c:\\Users\\Thiago\\Desktop\\final programacion\\quiz_api")
    
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}VERIFICACIÓN FINAL DEL PROYECTO{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    
    all_ok = True
    
    # Verificar estructura
    print(f"{BOLD}📁 ESTRUCTURA DEL PROYECTO:{RESET}")
    all_ok &= check_directory("app", "Paquete principal")
    all_ok &= check_directory("app/models", "Modelos SQLAlchemy")
    all_ok &= check_directory("app/schemas", "Schemas Pydantic")
    all_ok &= check_directory("app/routers", "Routers de API")
    all_ok &= check_directory("app/services", "Servicios de negocio")
    
    # Verificar archivos principales
    print(f"\n{BOLD}📄 ARCHIVOS PRINCIPALES:{RESET}")
    all_ok &= check_file("app/__init__.py", "Paquete app")
    all_ok &= check_file("app/main.py", "Aplicación FastAPI")
    all_ok &= check_file("app/database.py", "Configuración BD")
    
    # Verificar modelos
    print(f"\n{BOLD}📊 MODELOS SQLALCHEMY:{RESET}")
    all_ok &= check_file("app/models/__init__.py")
    all_ok &= check_file("app/models/question.py", "Modelo Question")
    all_ok &= check_file("app/models/quiz_session.py", "Modelo QuizSession")
    all_ok &= check_file("app/models/answer.py", "Modelo Answer")
    
    # Verificar schemas
    print(f"\n{BOLD}🔄 SCHEMAS PYDANTIC:{RESET}")
    all_ok &= check_file("app/schemas/__init__.py")
    all_ok &= check_file("app/schemas/question.py", "Schemas de preguntas")
    all_ok &= check_file("app/schemas/quiz_session.py", "Schemas de sesiones")
    all_ok &= check_file("app/schemas/answer.py", "Schemas de respuestas")
    
    # Verificar routers
    print(f"\n{BOLD}🛣️  ROUTERS API:{RESET}")
    all_ok &= check_file("app/routers/__init__.py")
    all_ok &= check_file("app/routers/questions.py", "Endpoints Questions")
    all_ok &= check_file("app/routers/quiz_sessions.py", "Endpoints Sessions")
    all_ok &= check_file("app/routers/answers.py", "Endpoints Answers")
    all_ok &= check_file("app/routers/statistics.py", "Endpoints Statistics")
    
    # Verificar servicios
    print(f"\n{BOLD}⚙️  SERVICIOS:{RESET}")
    all_ok &= check_file("app/services/__init__.py")
    all_ok &= check_file("app/services/quiz_service.py", "Lógica de negocio")
    
    # Verificar configuración
    print(f"\n{BOLD}⚙️  CONFIGURACIÓN:{RESET}")
    all_ok &= check_file("requirements.txt", "Dependencias")
    all_ok &= check_file(".env.example", "Variables de entorno")
    all_ok &= check_file(".gitignore", "Gitignore")
    
    # Verificar base de datos
    print(f"\n{BOLD}🗄️  BASE DE DATOS:{RESET}")
    all_ok &= check_file("quiz_api.db", "SQLite con datos")
    
    # Verificar documentación
    print(f"\n{BOLD}📚 DOCUMENTACIÓN:{RESET}")
    all_ok &= check_file("README.md", "Documentación principal")
    all_ok &= check_file("TESTING.md", "Resultados de pruebas")
    all_ok &= check_file("CHECKLIST.md", "Lista de verificación")
    all_ok &= check_file("INSTRUCCIONES.md", "Guía para GitHub")
    all_ok &= check_file("RESUMEN_ENTREGA.md", "Resumen de entrega")
    all_ok &= check_file("START_HERE.md", "Guía rápida")
    
    # Verificar scripts
    print(f"\n{BOLD}🧪 SCRIPTS:{RESET}")
    all_ok &= check_file("init_db.py", "Generador de datos")
    all_ok &= check_file("test_simple.py", "Tests simple")
    all_ok &= check_file("test_api.py", "Tests completo")
    all_ok &= check_file("setup_git.py", "Setup de Git")
    
    # Verificar que se pueden importar módulos
    print(f"\n{BOLD}✓ VERIFICACIÓN DE IMPORTS:{RESET}")
    try:
        sys.path.insert(0, '.')
        from app.database import init_db, get_db
        print(f"  {GREEN}✓{RESET} database.py - OK")
        
        from app.models.question import Question
        print(f"  {GREEN}✓{RESET} Question model - OK")
        
        from app.models.quiz_session import QuizSession
        print(f"  {GREEN}✓{RESET} QuizSession model - OK")
        
        from app.models.answer import Answer
        print(f"  {GREEN}✓{RESET} Answer model - OK")
        
        from app.schemas.question import QuestionCreate
        print(f"  {GREEN}✓{RESET} Question schemas - OK")
        
        from app.services.quiz_service import QuizService
        print(f"  {GREEN}✓{RESET} QuizService - OK")
        
        from app.main import app
        print(f"  {GREEN}✓{RESET} FastAPI app - OK")
        
    except Exception as e:
        print(f"  {RED}✗{RESET} Error en imports: {e}")
        all_ok = False
    
    # Resumen final
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    if all_ok:
        print(f"{BOLD}{GREEN}✓ VERIFICACIÓN COMPLETADA - TODO CORRECTO{RESET}")
        print(f"{BOLD}{GREEN}El proyecto está listo para entrega.{RESET}")
    else:
        print(f"{BOLD}{RED}✗ VERIFICACIÓN COMPLETADA CON PROBLEMAS{RESET}")
        print(f"{BOLD}{RED}Por favor revisa los archivos marcados con ✗{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
