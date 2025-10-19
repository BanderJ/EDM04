@echo off
REM Script para iniciar la aplicación Flask - Frutos de Oro
REM Este script activa el entorno virtual y ejecuta la aplicación

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                    🍓 FRUTOS DE ORO - INICIALIZADOR                   ║
echo ║              Sistema de Gestión de Cumplimiento Normativo             ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si el entorno virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Entorno virtual no encontrado
    echo.
    echo Crea el entorno virtual con:
    echo    python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Verificar si config.py existe
if not exist "config.py" (
    echo ❌ Archivo config.py no encontrado
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [1/3] Activando entorno virtual...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Error al activar el entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado
echo.

REM Verificar conexión a MySQL
echo [2/3] Verificando conexión a MySQL en puerto 3307...
netstat -ano | findstr ":3307" >nul 2>&1

if errorlevel 1 (
    echo.
    echo ⚠️  ADVERTENCIA: MySQL NO está disponible en puerto 3307
    echo.
    echo Soluciones:
    echo   1. Abre XAMPP Control Panel
    echo   2. Haz click en 'Start' para MySQL
    echo   3. Espera a que muestre 'Running' en puerto 3307
    echo   4. Ejecuta este script nuevamente
    echo.
    echo La aplicación continuará sin base de datos...
    echo.
    pause
) else (
    echo ✅ MySQL disponible en puerto 3307
    echo.
)

REM Iniciar la aplicación
echo [3/3] Iniciando aplicación Flask...
echo.
echo ═══════════════════════════════════════════════════════════════════════
echo   🌐 Accesible en: http://localhost:5000
echo   📝 Presiona Ctrl+C para detener la aplicación
echo ═══════════════════════════════════════════════════════════════════════
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ❌ Error al iniciar la aplicación
    echo Verifica los archivos de configuración
    pause
)

pause
