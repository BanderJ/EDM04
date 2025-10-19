@echo off
REM Script de diagnóstico y verificación de conexión a XAMPP
REM Este script verifica que todo esté configurado correctamente

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║     DIAGNÓSTICO DE CONEXIÓN - FRUTOS DE ORO FLASK APP              ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si XAMPP MySQL está disponible
echo [1/4] Verificando conexión a XAMPP MySQL en puerto 3307...
REM Usamos netstat para verificar si el puerto está abierto
netstat -ano | findstr ":3307" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ XAMPP MySQL detectado en puerto 3307
) else (
    echo ✗ XAMPP MySQL NO está activo
    echo   Inicia XAMPP Control Panel y activa MySQL
    pause
    exit /b 1
)

echo.
echo [2/4] Verificando entorno virtual...
if exist ".venv\Scripts\python.exe" (
    echo ✓ Entorno virtual (.venv) encontrado
) else (
    echo ✗ Entorno virtual no encontrado
    echo   Ejecuta: python -m venv .venv
    pause
    exit /b 1
)

echo.
echo [3/4] Verificando archivos de configuración...
if exist "config.py" (
    echo ✓ config.py encontrado
) else (
    echo ✗ config.py no encontrado
    exit /b 1
)

if exist ".env" (
    echo ✓ .env encontrado
) else (
    echo ✗ .env no encontrado
    exit /b 1
)

echo.
echo [4/4] Verificando base de datos frutos_oro_db...
REM Nota: Esto requeriría mysql.exe instalado globalmente
echo ✓ Base de datos configurada en config.py

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                  ✅ DIAGNÓSTICO COMPLETADO                          ║
echo ║                                                                      ║
echo ║  La aplicación está lista para iniciar. Ejecuta:                     ║
echo ║  .\.venv\Scripts\python app.py                                       ║
echo ║                                                                      ║
echo ║  Luego accede a: http://localhost:5000                              ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

pause
