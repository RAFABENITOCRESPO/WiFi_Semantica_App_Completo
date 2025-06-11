
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

def _load_points(ciudad: str, consulta: str | None = None):
    puntos = []
    consulta_lower = consulta.lower() if consulta else None
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
        estado = g.value(punto, WIFI.estado)

        if lat and lon:
            punto_data = {
                "ssid": str(ssid),
                "lat": float(lat),
                "long": float(lon),
                "seguridad": str(seguridad),
                "proveedor": str(proveedor),
            }
            if estado:
                punto_data["estado"] = str(estado)

            if consulta_lower:
                # Filtros simples para la interfaz
                if consulta_lower == "abierto" and str(seguridad).lower() != "abierto":
                    continue
                elif consulta_lower == "activos" and str(estado).lower() != "activo":
                    continue
                elif consulta_lower == "inactivos" and str(estado).lower() != "inactivo":
                    continue
                elif consulta_lower in {"wpa2", "wpa3", "wep", "abierto"}:
                    if consulta_lower != str(seguridad).lower():
                        continue
                else:
                    if consulta != str(proveedor):
                        continue
            puntos.append(punto_data)
    return puntos

@app.get("/api/puntos")
def puntos(ciudad: str, consulta: str | None = None):
    return JSONResponse(content=_load_points(ciudad, consulta))


@app.get("/api/run_query")
def run_query(name: str):
    """Execute a SPARQL query from the backend/queries folder."""
    query_path = os.path.join(ROOT_DIR, "../backend/queries", f"{name}.rq")
    if not os.path.isfile(query_path):
        return JSONResponse(status_code=404, content={"error": "Query not found"})

    with open(query_path, "r", encoding="utf-8") as f:
        sparql = f.read()

    results = g.query(sparql)
    rows = [{str(var): str(row[var]) for var in row.labels} for row in results]
    return JSONResponse(content=rows)
