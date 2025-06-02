
@echo off
cd /d %~dp0
echo [+] Activando entorno virtual...
call env\Scripts\activate.bat
echo [+] Lanzando API en http://127.0.0.1:8000
start http://127.0.0.1:8000/docs
uvicorn api.main:app --reload
pause
