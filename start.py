#!/usr/bin/env python3
"""
Script de inicio rápido para el Club Deportivo
Este script verifica las dependencias y ejecuta la aplicación
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Verificar que la versión de Python sea compatible"""
    if sys.version_info < (3, 7):
        print("[ERROR] Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"[OK] Python {sys.version.split()[0]} detectado")
    return True

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    try:
        import flask
        import flask_login
        import flask_sqlalchemy
        import flask_wtf
        import reportlab
        print("[OK] Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"[ERROR] Dependencia faltante: {e}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False

def check_database():
    """Verificar si la base de datos existe"""
    db_path = Path("club_deportivo.db")
    if db_path.exists():
        print("[OK] Base de datos encontrada")
        return True
    else:
        print("[WARN] Base de datos no encontrada")
        return False

def create_database():
    """Crear la base de datos automáticamente"""
    try:
        print("[INFO] Creando base de datos...")
        from init_db import create_sample_data
        create_sample_data()
        print("[OK] Base de datos creada exitosamente")
        return True
    except Exception as e:
        print(f"[ERROR] Error al crear la base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("Club Deportivo - Verificación del Sistema")
    print("=" * 50)
    
    # Verificaciones básicas
    python_ok = check_python_version()
    venv_ok = check_virtual_env()
    deps_ok = check_dependencies()
    db_ok = check_database()
    
    print("\n" + "=" * 50)
    
    # Si las dependencias están bien pero falta la base de datos
    if python_ok and deps_ok and not db_ok:
        print("[INFO] Base de datos faltante detectada")
        print("[INFO] Creando base de datos automáticamente...")
        if create_database():
            db_ok = True
        else:
            print("[ERROR] No se pudo crear la base de datos automáticamente")
            print("   Ejecuta manualmente: python init_db.py")
    
    # Verificaciones finales
    checks = [python_ok, deps_ok, db_ok]
    
    if all(checks):
        print("\n[SUCCESS] ¡Todo listo! Iniciando la aplicación...")
        print("[INFO] La aplicación estará disponible en: http://localhost:5000")
        print("[INFO] Presiona Ctrl+C para detener la aplicación")
        print("\nUsuarios de prueba disponibles:")
        print("   Admin: admin / admin123")
        print("   Entrenadores: carlos.trainer, ana.trainer, luis.trainer / trainer123")
        print("   Miembros: juan.member, maria.member, pedro.member, laura.member, diego.member / member123")
        print("\n" + "=" * 50)
        
        # Ejecutar la aplicación
        try:
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except KeyboardInterrupt:
            print("\n[INFO] ¡Hasta luego!")
        except Exception as e:
            print(f"\n[ERROR] Error al iniciar la aplicación: {e}")
    else:
        print("\n[ERROR] Algunas verificaciones fallaron. Por favor, corrige los errores antes de continuar.")
        print("\nPasos recomendados:")
        if not python_ok:
            print("   1. Actualizar Python a versión 3.7 o superior")
        if not venv_ok:
            print("   2. Crear entorno virtual: python -m venv venv")
            print("   3. Activar entorno virtual: venv\\Scripts\\activate (Windows) o source venv/bin/activate (Linux/Mac)")
        if not deps_ok:
            print("   4. Instalar dependencias: pip install -r requirements.txt")
        if not db_ok:
            print("   5. Inicializar base de datos: python init_db.py")
        print("   6. Ejecutar aplicación: python app.py")

if __name__ == "__main__":

    main()
