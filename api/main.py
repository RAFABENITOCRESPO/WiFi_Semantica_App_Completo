
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rdflib import Graph, Namespace, RDF
from pyproj import Transformer
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="public"), name="static")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Ajusta según estructura, dos niveles arriba

@app.get("/")
async def read_index():
    return FileResponse(BASE_DIR / "public" / "index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

wifi_ns = Namespace("http://example.org/wifi#")

# Cargar los grafos RDF
g_ba = Graph()
g_ny = Graph()

g_ba.parse("backend/ontology/buenos_aires_wifi.rdf", format="xml")
print("[INFO] RDF de Buenos Aires cargado.")
g_ny.parse("backend/ontology/final_individuos_ny.rdf", format="xml")
print("[INFO] RDF de New York cargado.")

@app.get("/api/puntos")
async def get_puntos(ciudad: str = "", consulta: str = "todos"):
    resultados = []

    grafo = g_ba if ciudad.lower() == "buenosaires" else g_ny

    for s in grafo.subjects(RDF.type, wifi_ns.PuntoDeAccesoWiFi):
        ssid = grafo.value(s, wifi_ns.ssid)
        lat = grafo.value(s, wifi_ns.latitud)
        lon = grafo.value(s, wifi_ns.longitud)
        estado = grafo.value(s, wifi_ns.estado)
        proveedor = grafo.value(s, wifi_ns.proveedor)
        seguridad = grafo.value(s, wifi_ns.seguridad)

        print(f"[DEBUG] ssid={ssid} lat={lat} lon={lon} estado={estado} proveedor={proveedor} seguridad={seguridad}")

        if lat and lon:
            try:
                punto_data = {
                    "ssid": str(ssid) if ssid else "",
                    "lat": float(lat),
                    "long": float(lon),
                    "estado": str(estado) if estado else "",
                    "proveedor": str(proveedor) if proveedor else "",
                    "seguridad": str(seguridad) if seguridad else ""
                }
                resultados.append(punto_data)
            except Exception as e:
                print(f"[ERROR] Problema procesando {s}: {e}")

    return JSONResponse(content=resultados)
