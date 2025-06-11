
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from rdflib import Graph, Namespace
from rdflib.namespace import RDF
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta base del archivo index.html
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
DATA_PATH = os.path.join(ROOT_DIR, "data", "wifi_ontology_combined.owl")

# Cargar ontología
g = Graph()
g.parse(DATA_PATH, format="xml")

# Namespaces
WIFI = Namespace("http://example.org/wifi#")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

def get_value(s, p):
    val = g.value(s, p)
    return val.toPython() if val else None

@app.get("/")
def index():
    return FileResponse(INDEX_PATH, media_type="text/html")

@app.get("/api/consulta")
def consulta_general(ciudad: str, consulta: str = "todos"):
    resultado = []

    for s in g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi):
        ciudad_val = get_value(s, WIFI.ubicadoEnCiudad)
        if ciudad_val != ciudad:
            continue

        proveedor = get_value(s, WIFI.proveedor)
        seguridad = get_value(s, WIFI.seguridad)
        estado = get_value(s, WIFI.estado)
        tipo = get_value(s, WIFI.tipo)

        if consulta == "todos":
            pass
        elif consulta == "abierto" and seguridad != "Abierto":
            continue
        elif consulta == "activos" and estado != "Activo":
            continue
        elif consulta == "inactivos" and estado != "Inactivo":
            continue
        elif consulta.lower() in ["wpa2", "wpa3", "wep", "abierto"] and seguridad.lower() != consulta.lower():
            continue
        elif consulta in ["Gobierno_BA", "Starbucks_Corporation"] and proveedor != consulta:
            continue
        elif consulta.lower() in ["publico", "privado", "municipal", "comercial"] and tipo and tipo.lower() != consulta.lower():
            continue

        resultado.append({
            "nombre": get_value(s, WIFI.nombre),
            "calle": get_value(s, WIFI.calle),
            "barrio": get_value(s, WIFI.barrio),
            "comuna": get_value(s, WIFI.comuna),
            "proveedor": proveedor,
            "seguridad": seguridad,
            "latitud": get_value(s, GEO.lat),
            "longitud": get_value(s, GEO.long)
        })

    return resultado


@app.get("/api/consulta/seguridad_debil")
def consulta_seguridad_debil(ciudad: str):
    """Return hotspots with weak security (WEP) for the given city."""
    resultado = []

    for s in g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi):
        if get_value(s, WIFI.ubicadoEnCiudad) != ciudad:
            continue

        seguridad = get_value(s, WIFI.seguridad)
        if seguridad and seguridad.lower() == "wep":
            resultado.append({
                "nombre": get_value(s, WIFI.nombre),
                "calle": get_value(s, WIFI.calle),
                "barrio": get_value(s, WIFI.barrio),
                "comuna": get_value(s, WIFI.comuna),
                "proveedor": get_value(s, WIFI.proveedor),
                "seguridad": seguridad,
                "latitud": get_value(s, GEO.lat),
                "longitud": get_value(s, GEO.long)
            })

    return resultado