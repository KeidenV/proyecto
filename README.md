# Sistema de Gestión de Club Deportivo

Una plataforma completa para administrar miembros, entrenamientos y competiciones en un club deportivo.

## 🚀 Características

### Roles y Permisos
- **Administrador**: Acceso completo al sistema, gestión de usuarios, reportes
- **Entrenador**: Gestión de entrenamientos, registro de asistencias
- **Miembro**: Visualización de entrenamientos, historial personal

### Funcionalidades Principales
- ✅ Sistema de autenticación con Flask-Login
- ✅ CRUD completo para miembros, entrenadores y actividades
- ✅ Registro de entrenamientos y asistencia
- ✅ Calendario de competiciones y eventos
- ✅ Generación de reportes PDF
- ✅ Interfaz moderna y responsive
- ✅ Manejo de errores 404 y 500

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Base de Datos**: MySQL (con PyMySQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Reportes**: ReportLab para generación de PDFs
- **Formularios**: Flask-WTF, WTForms

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd club-deportivo
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar MySQL
Asegúrate de tener MySQL instalado y ejecutándose, luego:

```bash
# Configurar la base de datos MySQL
python setup_mysql.py
```

### 6. Inicializar base de datos con datos de ejemplo
```bash
python init_db.py
```

### 7. Ejecutar la aplicación
```bash
python start.py
```

La aplicación estará disponible en `http://localhost:5000`

## ⚙️ Configuración de MySQL

### Requisitos
- MySQL 5.7+ o MariaDB 10.3+
- Usuario con permisos para crear bases de datos

### Configuración automática
El script `setup_mysql.py` configurará automáticamente la base de datos. Asegúrate de cambiar las credenciales en el archivo si es necesario:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'tu_contraseña'
MYSQL_DATABASE = 'club_deportivo'
```

### Configuración manual
Si prefieres configurar manualmente:

1. Crea la base de datos:
```sql
CREATE DATABASE club_deportivo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Ejecuta el script SQL:
```bash
mysql -u root -p club_deportivo < db.sql
```

3. Configura las variables de entorno o edita `config.py`

## 👥 Usuarios de Prueba

Después de ejecutar `init_db.py`, tendrás estos usuarios disponibles:

### Administrador
- **Email**: `admin@club.com` / **Contraseña**: `admin123`

### Entrenadores
- **Email**: `carlos@club.com` / **Contraseña**: `trainer123`
- **Email**: `ana@club.com` / **Contraseña**: `trainer123`
- **Email**: `luis@club.com` / **Contraseña**: `trainer123`

### Miembros
- **Email**: `juan@club.com` / **Contraseña**: `member123`
- **Email**: `maria@club.com` / **Contraseña**: `member123`
- **Email**: `pedro@club.com` / **Contraseña**: `member123`
- **Email**: `laura@club.com` / **Contraseña**: `member123`
- **Email**: `diego@club.com` / **Contraseña**: `member123`

## 📁 Estructura del Proyecto

```
club-deportivo/
├── app.py                 # Aplicación principal
├── models.py              # Modelos de base de datos
├── forms.py               # Formularios WTForms
├── init_db.py             # Script de inicialización
├── requirements.txt       # Dependencias
├── routes/                # Rutas de la aplicación
│   ├── auth.py           # Autenticación
│   ├── admin.py          # Panel de administración
│   ├── trainer.py        # Funcionalidades de entrenador
│   ├── member.py         # Funcionalidades de miembro
│   ├── main.py           # Rutas principales
│   └── reports.py        # Generación de reportes
├── templates/             # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página de inicio
│   ├── calendar.html      # Calendario de eventos
│   ├── auth/             # Templates de autenticación
│   ├── admin/            # Templates de administración
│   ├── trainer/          # Templates de entrenador
│   ├── member/           # Templates de miembro
│   └── errors/          # Templates de errores
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── main.js       # JavaScript personalizado
```

## 🔧 Configuración

### Variables de Entorno
Puedes configurar estas variables en `app.py`:

```python
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club_deportivo.db'
```

### Base de Datos
El sistema usa MySQL por defecto. La configuración se maneja a través de `config.py`:

```python
# Desarrollo (MySQL)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/club_deportivo'

# Producción (MySQL)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/club_deportivo'

# Testing (SQLite en memoria)
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### Variables de Entorno
Puedes configurar la aplicación usando variables de entorno:

```bash
export FLASK_ENV=development
export MYSQL_USER=root
export MYSQL_PASSWORD=tu_contraseña
export MYSQL_HOST=localhost
export MYSQL_DATABASE=club_deportivo
```

## 📊 Funcionalidades por Rol

### 👑 Administrador
- Dashboard con estadísticas generales
- Gestión completa de miembros
- Gestión completa de entrenadores
- Gestión de entrenamientos
- Gestión de competiciones
- Generación de reportes PDF
- Acceso a todas las funcionalidades

### 🏃 Entrenador
- Dashboard personal con estadísticas
- Gestión de sus entrenamientos
- Registro de asistencias
- Visualización de miembros
- Edición de perfil personal

### 👥 Miembro
- Dashboard personal
- Visualización de entrenamientos disponibles
- Historial de asistencias
- Información de competiciones
- Edición de perfil personal

## 📈 Reportes Disponibles

1. **Historial de Entrenamientos por Miembro**
   - Información personal del miembro
   - Lista completa de asistencias
   - Estadísticas de asistencia

2. **Reporte de Asistencia General**
   - Resumen por entrenamiento
   - Detalle de asistencias por período
   - Estadísticas generales

3. **Resultados de Competiciones**
   - Información de la competición
   - Detalles del evento
   - Notas sobre resultados

## 🎨 Personalización

### Estilos CSS
Los estilos personalizados están en `static/css/style.css`. Puedes modificar:
- Colores principales
- Tipografías
- Espaciados
- Animaciones

### Templates HTML
Los templates usan Bootstrap 5 y pueden ser personalizados fácilmente.

## 🚨 Manejo de Errores

El sistema incluye manejo de errores para:
- **404**: Página no encontrada
- **500**: Error interno del servidor
- Errores de validación de formularios
- Errores de base de datos

## 🔒 Seguridad

- Autenticación con Flask-Login
- Contraseñas hasheadas con Werkzeug
- Validación de formularios con WTForms
- Protección CSRF
- Control de acceso por roles

## 📱 Responsive Design

La interfaz es completamente responsive y funciona en:
- Desktop
- Tablet
- Móvil

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🔄 Actualizaciones Futuras

- [ ] Notificaciones por email
- [ ] Sistema de pagos
- [ ] App móvil
- [ ] Integración con redes sociales
- [ ] Sistema de reservas online
- [ ] Chat en tiempo real
- [ ] Dashboard con gráficos avanzados

---

**Desarrollado con ❤️ para la gestión deportiva**
