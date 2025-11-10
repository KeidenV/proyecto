<#
start_project.ps1
Script para Windows PowerShell que automatiza:
 1. Crear entorno virtual (si no existe)
 2. Activarlo
 3. Instalar dependencias desde requirements.txt
 4. Inicializar la base de datos (init_db.py)
 5. Ejecutar la aplicación (app.py)

Uso: Ejecutar desde la carpeta del proyecto con PowerShell:
  .\start_project.ps1

Nota: Puede ser necesario ejecutar PowerShell con permisos o ajustar ExecutionPolicy:
  PowerShell -ExecutionPolicy Bypass -File .\start_project.ps1
#>

Write-Host "== Inicio del script de puesta en marcha del proyecto ==" -ForegroundColor Cyan
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectRoot

# 1) Verificar python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] No se encontró 'python' en el PATH. Instala Python 3.7+ y vuelve a intentarlo." -ForegroundColor Red
    exit 1
}

# 2) Crear entorno virtual si no existe
$venvPath = Join-Path $projectRoot "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "[INFO] Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
} else {
    Write-Host "[OK] Entorno virtual ya existe" -ForegroundColor Green
}

# 3) Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "[ERROR] No se encontró el script de activación: $activateScript" -ForegroundColor Red
    exit 1
}

# 4) Instalar dependencias
if (Test-Path "requirements.txt") {
    Write-Host "[INFO] Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "[WARN] No se encontró requirements.txt. Saltando instalación de dependencias." -ForegroundColor Yellow
}

# 5) Inicializar base de datos
if (Test-Path "init_db.py") {
    Write-Host "[INFO] Inicializando base de datos..." -ForegroundColor Yellow
    python init_db.py
} else {
    Write-Host "[WARN] No se encontró init_db.py. Saltando inicialización de la base de datos." -ForegroundColor Yellow
}

# 6) Ejecutar aplicación
if (Test-Path "app.py") {
    Write-Host "[INFO] Iniciando la aplicación (Ctrl+C para detener)..." -ForegroundColor Cyan
    python app.py
} else {
    Write-Host "[ERROR] No se encontró app.py. No se puede iniciar la aplicación." -ForegroundColor Red
    exit 1
}
