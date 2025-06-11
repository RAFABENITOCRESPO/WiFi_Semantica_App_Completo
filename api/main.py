
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "../public")

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/api/consulta")
def consulta(ciudad: str, consulta: str):
    # Devolver datos de ejemplo
    if ciudad.lower() == "buenos aires":
        return JSONResponse(content=[
            {"nombre": "WiFi Plaza", "latitud": -34.6037, "longitud": -58.3816},
            {"nombre": "WiFi Parque", "latitud": -34.6090, "longitud": -58.3922}
        ])
    elif ciudad.lower() == "new york":
        return JSONResponse(content=[
            {"nombre": "WiFi Central Park", "latitud": 40.7812, "longitud": -73.9665},
            {"nombre": "WiFi Times Square", "latitud": 40.7580, "longitud": -73.9855}
        ])
    else:
        return JSONResponse(content=[])
