@echo off
REM ====================================================
REM SCRIPT DE INSTALACION - Frutos de Oro S.A.C.
REM Sistema de Gestion de Cumplimiento Normativo
REM Para Windows
REM ====================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo    FRUTOS DE ORO - Sistema de Gestion de Cumplimiento Normativo
echo    Script de Instalacion
echo ================================================================================
echo.

REM Verificar si Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version

REM Crear entorno virtual
echo.
echo [*] Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo [*] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo [*] Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas correctamente

REM Crear archivo .env
echo.
echo [*] Creando archivo de configuracion...
if not exist .env (
    copy .env.example .env
    echo [OK] Archivo .env creado
    echo [IMPORTANTE] Edita el archivo .env con tus configuraciones
) else (
    echo [OK] El archivo .env ya existe
)

REM Crear carpetas necesarias
echo [*] Creando carpetas necesarias...
if not exist uploads mkdir uploads
if not exist uploads\certifications mkdir uploads\certifications
if not exist logs mkdir logs

REM Información de base de datos
echo.
echo ================================================================================
echo    CONFIGURACION DE BASE DE DATOS
echo ================================================================================
echo.
echo El sistema necesita una base de datos. Elige una opcion:
echo.
echo 1) MySQL (recomendado para este proyecto)
echo 2) PostgreSQL
echo 3) SQLite (desarrollo solamente)
echo.

REM Crear base de datos de ejemplo en SQLite (para desarrollo rápido)
echo [*] Para desarrollo rápido, se usará SQLite
set DATABASE_URL=sqlite:///frutos_oro_dev.db

REM Información sobre cómo ejecutar
echo.
echo ================================================================================
echo    INSTALACION COMPLETADA
echo ================================================================================
echo.
echo Para ejecutar la aplicacion:
echo.
echo 1. Abre una terminal en esta carpeta
echo 2. Ejecuta: venv\Scripts\activate.bat
echo 3. Luego: python app.py
echo.
echo La aplicacion se abrirá en: http://localhost:5000
echo.
echo Credenciales de acceso:
echo   Usuario: admin
echo   Contraseña: admin123
echo.
echo ================================================================================
echo.
echo Presiona cualquier tecla para continuar...
pause

REM Iniciar la aplicación
echo.
echo [*] Iniciando aplicacion...
python app.py
