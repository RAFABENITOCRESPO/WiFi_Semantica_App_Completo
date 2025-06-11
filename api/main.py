
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rdflib import Graph, Namespace, RDF
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
ONTOLOGY_PATH = os.path.join(ROOT_DIR, "../backend/ontology/ontology.owl")

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

WIFI = Namespace("http://www.semanticweb.org/ontowifi#")
g = Graph()
g.parse(ONTOLOGY_PATH, format="xml")

def _load_points(ciudad: str):
    puntos = []
    for punto in g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi):
        ubicacion = g.value(punto, WIFI.tieneUbicacion)
        if ubicacion is None:
            continue
        ciudad_val = g.value(ubicacion, WIFI.ciudad)
        if ciudad_val is None or ciudad.lower() not in str(ciudad_val).lower():
            continue

        ssid = g.value(punto, WIFI.nombreSSID)
        lat = g.value(ubicacion, WIFI.latitud)
        lon = g.value(ubicacion, WIFI.longitud)
        seguridad = g.value(punto, WIFI.usaSeguridad)
        proveedor = g.value(punto, WIFI.esOperadoPor)

        if lat and lon:
            puntos.append({
                "ssid": str(ssid),
                "lat": float(lat),
                "long": float(lon),
                "seguridad": str(seguridad),
                "proveedor": str(proveedor),
            })
    return puntos

@app.get("/api/puntos")
def puntos(ciudad: str):
    return JSONResponse(content=_load_points(ciudad))
