@echo off
echo ---------------------------------------------
echo Inicializando entorno virtual y servidor API
echo ---------------------------------------------

REM Paso 1: Crear entorno virtual si no existe
IF NOT EXIST "env" (
    echo Creando entorno virtual...
    python -m venv env
)

REM Paso 2: Activar entorno virtual
call env\Scripts\activate

REM Paso 3: Instalar dependencias
echo Instalando dependencias necesarias...
pip install --upgrade pip
pip install fastapi uvicorn rdflib

REM Paso 4: Lanzar servidor
echo Lanzando servidor en http://localhost:8000
cd api
uvicorn main:app --reload
pause
