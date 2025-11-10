#!/usr/bin/env python3
"""
Script para inicializar la base de datos del Club Deportivo
Crea datos de ejemplo para testing y demostración
"""

from app import app, db
from models import Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash

def create_sample_data():
    """Crear datos de ejemplo para el club deportivo"""
    
    with app.app_context():
        # Limpiar base de datos existente
        db.drop_all()
        db.create_all()
        
        print("Creando datos de ejemplo...")
        
        # 1. Crear roles
        roles_data = [
            {'nombre_rol': 'Administrador'},
            {'nombre_rol': 'Entrenador'},
            {'nombre_rol': 'Miembro'}
        ]
        
        roles = []
        for rol_data in roles_data:
            rol = Rol(**rol_data)
            db.session.add(rol)
            roles.append(rol)
        
        db.session.flush()  # Para obtener los IDs de los roles
        
        # 2. Crear actividades deportivas
        actividades_data = [
            {'nombre_actividad': 'Fútbol'},
            {'nombre_actividad': 'Natación'},
            {'nombre_actividad': 'Básquetbol'},
            {'nombre_actividad': 'Tenis'},
            {'nombre_actividad': 'Atletismo'}
        ]
        
        actividades = []
        for actividad_data in actividades_data:
            actividad = Actividad(**actividad_data)
            db.session.add(actividad)
            actividades.append(actividad)
        
        db.session.flush()  # Para obtener los IDs de las actividades
        
        # 3. Crear usuarios administradores
        admin_user = Usuario(
            nombre='Administrador',
            apellido='Sistema',
            email='admin@club.com',
            fecha_nacimiento=date(1980, 1, 1),
            id_rol=roles[0].id_rol  # Administrador
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # 4. Crear entrenadores
        entrenadores_data = [
            {
                'nombre': 'Carlos',
                'apellido': 'Mendoza',
                'email': 'carlos@club.com',
                'fecha_nacimiento': date(1985, 3, 15),
                'id_rol': roles[1].id_rol  # Entrenador
            },
            {
                'nombre': 'Ana',
                'apellido': 'Rodríguez',
                'email': 'ana@club.com',
                'fecha_nacimiento': date(1988, 7, 22),
                'id_rol': roles[1].id_rol  # Entrenador
            },
            {
                'nombre': 'Luis',
                'apellido': 'García',
                'email': 'luis@club.com',
                'fecha_nacimiento': date(1982, 11, 8),
                'id_rol': roles[1].id_rol  # Entrenador
            }
        ]
        
        entrenadores = []
        for entrenador_data in entrenadores_data:
            entrenador = Usuario(**entrenador_data)
            entrenador.set_password('trainer123')
            db.session.add(entrenador)
            entrenadores.append(entrenador)
        
        # 5. Crear miembros
        miembros_data = [
            {
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'email': 'juan@club.com',
                'fecha_nacimiento': date(1990, 5, 15),
                'id_rol': roles[2].id_rol  # Miembro
            },
            {
                'nombre': 'María',
                'apellido': 'López',
                'email': 'maria@club.com',
                'fecha_nacimiento': date(1985, 8, 22),
                'id_rol': roles[2].id_rol  # Miembro
            },
            {
                'nombre': 'Pedro',
                'apellido': 'Martínez',
                'email': 'pedro@club.com',
                'fecha_nacimiento': date(1992, 12, 3),
                'id_rol': roles[2].id_rol  # Miembro
            },
            {
                'nombre': 'Laura',
                'apellido': 'González',
                'email': 'laura@club.com',
                'fecha_nacimiento': date(1988, 3, 18),
                'id_rol': roles[2].id_rol  # Miembro
            },
            {
                'nombre': 'Diego',
                'apellido': 'Hernández',
                'email': 'diego@club.com',
                'fecha_nacimiento': date(1995, 7, 7),
                'id_rol': roles[2].id_rol  # Miembro
            }
        ]
        
        miembros = []
        for miembro_data in miembros_data:
            miembro = Usuario(**miembro_data)
            miembro.set_password('member123')
            db.session.add(miembro)
            miembros.append(miembro)
        
        db.session.flush()  # Para obtener los IDs de los usuarios
        
        # 6. Crear entrenamientos
        entrenamientos_data = [
            {
                'id_entrenador': entrenadores[0].id_usuario,
                'id_actividad': actividades[0].id_actividad,  # Fútbol
                'fecha': date.today() + timedelta(days=1)
            },
            {
                'id_entrenador': entrenadores[1].id_usuario,
                'id_actividad': actividades[1].id_actividad,  # Natación
                'fecha': date.today() + timedelta(days=2)
            },
            {
                'id_entrenador': entrenadores[2].id_usuario,
                'id_actividad': actividades[2].id_actividad,  # Básquetbol
                'fecha': date.today() + timedelta(days=3)
            },
            {
                'id_entrenador': entrenadores[0].id_usuario,
                'id_actividad': actividades[0].id_actividad,  # Fútbol
                'fecha': date.today() + timedelta(days=4)
            },
            {
                'id_entrenador': entrenadores[1].id_usuario,
                'id_actividad': actividades[1].id_actividad,  # Natación
                'fecha': date.today() + timedelta(days=5)
            }
        ]
        
        entrenamientos = []
        for entrenamiento_data in entrenamientos_data:
            entrenamiento = Entrenamiento(**entrenamiento_data)
            db.session.add(entrenamiento)
            entrenamientos.append(entrenamiento)
        
        db.session.flush()  # Para obtener los IDs de los entrenamientos
        
        # 7. Crear competiciones
        competiciones_data = [
            {
                'nombre': 'Torneo de Fútbol Primavera',
                'fecha': date.today() + timedelta(days=30),
                'ubicacion': 'Complejo Deportivo Municipal',
                'descripcion': 'Torneo anual de fútbol para todas las categorías',
                'id_actividad': actividades[0].id_actividad  # Fútbol
            },
            {
                'nombre': 'Competencia de Natación',
                'fecha': date.today() + timedelta(days=45),
                'ubicacion': 'Piscina Olímpica',
                'descripcion': 'Competencia de natación en diferentes estilos',
                'id_actividad': actividades[1].id_actividad  # Natación
            },
            {
                'nombre': 'Liga de Básquetbol',
                'fecha': date.today() + timedelta(days=60),
                'ubicacion': 'Gimnasio Principal',
                'descripcion': 'Liga local de básquetbol',
                'id_actividad': actividades[2].id_actividad  # Básquetbol
            }
        ]
        
        competiciones = []
        for competicion_data in competiciones_data:
            competicion = Competicion(**competicion_data)
            db.session.add(competicion)
            competiciones.append(competicion)
        
        db.session.flush()  # Para obtener los IDs de las competiciones
        
        # 8. Crear asistencias de ejemplo
        fechas_asistencia = [
            date.today() - timedelta(days=1),
            date.today() - timedelta(days=2),
            date.today() - timedelta(days=3),
            date.today() - timedelta(days=7),
            date.today() - timedelta(days=8)
        ]
        
        for i, fecha_asistencia in enumerate(fechas_asistencia):
            # Crear entrenamientos pasados para las asistencias
            entrenamiento_pasado = Entrenamiento(
                id_entrenador=entrenadores[i % len(entrenadores)].id_usuario,
                id_actividad=actividades[i % len(actividades)].id_actividad,
                fecha=fecha_asistencia
            )
            db.session.add(entrenamiento_pasado)
            db.session.flush()
            
            # Crear asistencias para algunos miembros
            for j, miembro in enumerate(miembros[:3]):  # Solo los primeros 3 miembros
                asistencia = Asistencia(
                    id_entrenamiento=entrenamiento_pasado.id_entrenamiento,
                    id_miembro=miembro.id_usuario,
                    presente=True,
                    observaciones=f'Asistencia del {fecha_asistencia.strftime("%d/%m/%Y")}'
                )
                db.session.add(asistencia)
        
        # 9. Crear algunos resultados de competición
        for i, competicion in enumerate(competiciones):
            for j, miembro in enumerate(miembros[:2]):  # Solo los primeros 2 miembros
                resultado = ResultadoCompeticion(
                    id_competicion=competicion.id_competicion,
                    id_usuario=miembro.id_usuario,
                    posicion=j + 1,
                    marca=f'{i+1}:{(j+1)*10}:{(j+1)*5}',  # Tiempo ficticio
                    observaciones=f'Resultado en {competicion.nombre}'
                )
                db.session.add(resultado)
        
        # Guardar todos los cambios
        db.session.commit()
        
        print("[OK] Datos de ejemplo creados exitosamente!")
        print("\nUsuarios creados:")
        print("Administrador: admin@club.com / admin123")
        print("Entrenadores: carlos@club.com, ana@club.com, luis@club.com / trainer123")
        print("Miembros: juan@club.com, maria@club.com, pedro@club.com, laura@club.com, diego@club.com / member123")
        print(f"\nEstadísticas:")
        print(f"   - {len(roles)} roles")
        print(f"   - {len(actividades)} actividades")
        print(f"   - {len(entrenadores)} entrenadores")
        print(f"   - {len(miembros)} miembros")
        print(f"   - {len(entrenamientos)} entrenamientos")
        print(f"   - {len(competiciones)} competiciones")
        print(f"   - {len(fechas_asistencia) * 3} asistencias registradas")

if __name__ == '__main__':
    create_sample_data()
