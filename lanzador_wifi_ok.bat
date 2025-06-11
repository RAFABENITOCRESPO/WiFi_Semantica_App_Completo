@echo off
setlocal

echo ==== Entrando a la carpeta del proyecto ====
cd /d "%~dp0"

IF NOT EXIST env (
    echo ==== Creando entorno virtual ====
    python -m venv env
)

echo ==== Activando entorno virtual ====
call env\Scripts\activate.bat

echo ==== Instalando dependencias necesarias ====
pip install fastapi uvicorn rdflib python-dotenv

echo ==== Iniciando servidor FastAPI con Uvicorn ====
uvicorn api.main:app --reload --port 8000

pause