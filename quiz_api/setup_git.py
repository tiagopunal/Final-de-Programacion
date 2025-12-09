#!/usr/bin/env python3
"""
Script para inicializar el repositorio Git del proyecto.
Ejecutar: python setup_git.py
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Ejecuta un comando y reporta el resultado"""
    print(f"\n📋 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completado")
            if result.stdout:
                print(result.stdout[:200])
            return True
        else:
            print(f"✗ Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("CONFIGURACIÓN DE REPOSITORIO GIT")
    print("="*60)
    
    os.chdir("c:\\Users\\Thiago\\Desktop\\final programacion\\quiz_api")
    
    # Inicializar Git
    if not os.path.exists(".git"):
        run_command("git init", "Inicializar repositorio Git")
    else:
        print("✓ Repositorio Git ya existe")
    
    # Configurar usuario de Git
    run_command('git config user.name "Tu Nombre"', "Configurar nombre de usuario")
    run_command('git config user.email "tu.email@example.com"', "Configurar email")
    
    # Ver estado
    print("\n📊 Estado del repositorio:")
    run_command("git status", "Verificar estado")
    
    print("\n" + "="*60)
    print("✓ CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("\nProximos pasos:")
    print("1. Edita .gitignore si es necesario")
    print("2. Crea repositorio en GitHub")
    print("3. Ejecuta: git remote add origin <url-del-repositorio>")
    print("4. Ejecuta: git add .")
    print("5. Ejecuta: git commit -m 'Initial commit'")
    print("6. Ejecuta: git push -u origin main")
    print()

if __name__ == "__main__":
    main()
