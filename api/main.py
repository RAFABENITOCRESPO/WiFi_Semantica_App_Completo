
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, RDF
import os

app = FastAPI()

# Servir contenido estático desde /public

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FUSEKI_ENDPOINT = "http://localhost:3030/ontowifi/sparql"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "../public")
ONTOLOGY_PATH = os.path.join(ROOT_DIR, "../backend/ontology/ontology.owl")
print(f"[INFO] Cargando ontología desde: {ONTOLOGY_PATH}")


WIFI = Namespace("http://example.org/wifi#")
g = Graph()
g.parse(ONTOLOGY_PATH, format="xml")
print(f"[INFO] Ontología cargada con {len(g)} triples.")

def _load_points(ciudad: str, consulta: str | None = None):
    puntos = []
    consulta_lower = consulta.lower() if consulta else None
    for punto in g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi):
        ubicacion = g.value(punto, WIFI.tieneUbicacion)
        if ubicacion is None:
            continue
        ciudad_val = g.value(ubicacion, WIFI.ciudad)
        if ciudad_val is None or ciudad.lower().replace(" ", "").replace("_", "") not in str(ciudad_val).lower().replace(" ", "").replace("_", ""):
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

            if consulta_lower == "todos":
                puntos.append(punto_data)
                continue

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
                elif consulta_lower in {"publico", "privado", "municipal", "comercial"}:
                    clase_objetivo = WIFI[f"WiFi_{consulta.capitalize()}"]
                    if (punto, RDF.type, clase_objetivo) not in g:
                        continue
                else:
                    if consulta != str(proveedor):
                        continue

            puntos.append(punto_data)
    return puntos

def ejecutar_consulta(nombre_archivo: str):
    ruta = os.path.join("consultas", nombre_archivo)
    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    with open(ruta, "r", encoding="utf-8") as file:
        query = file.read()

    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/puntos")
def puntos(ciudad: str, consulta: str | None = None):
    return JSONResponse(content=_load_points(ciudad, consulta))

@app.get("/api/consulta/activos/buenosaires")
def activos_buenosaires():
    return ejecutar_consulta("consulta_activos_buenosaires.rq")

@app.get("/api/consulta/activos/newyork")
def activos_newyork():
    return ejecutar_consulta("consulta_activos_newyork.rq")

@app.get("/api/consulta/ciudad/buenosaires")
def ciudad_buenosaires():
    return ejecutar_consulta("consulta_ciudad_buenosaires.rq")

@app.get("/api/consulta/ciudad/newyork")
def ciudad_newyork():
    return ejecutar_consulta("consulta_ciudad_newyork.rq")

@app.get("/api/consulta/proveedor/gobiernoBA")
def proveedor_ba():
    return ejecutar_consulta("consulta_proveedor_gobiernoBA.rq")

@app.get("/api/consulta/proveedor/gobiernoNY")
def proveedor_ny():
    return ejecutar_consulta("consulta_proveedor_gobiernoNY.rq")

@app.get("/api/consulta/abiertos/buenosaires")
def abiertos_ba():
    return ejecutar_consulta("consulta_abiertos_buenosaires.rq")

@app.get("/api/consulta/abiertos/newyork")
def abiertos_ny():
    return ejecutar_consulta("consulta_abiertos_newyork.rq")

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

app.mount("/", StaticFiles(directory="public", html=True), name="static")