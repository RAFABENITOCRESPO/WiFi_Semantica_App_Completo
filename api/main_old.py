
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rdflib import Graph, Namespace, RDF
from pyproj import Transformer
import os

transformer = Transformer.from_crs("EPSG:22185", "EPSG:4326", always_xy=True)
GEO_NS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

# --- Configuración de la app ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Directorios del proyecto ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ONTOLOGY_PATH_BA = os.path.join(ROOT_DIR, "../backend/ontology/buenos_aires_wifi.owl")
ONTOLOGY_PATH_NY = os.path.join(ROOT_DIR, "../backend/ontology/nyc_wifi_public.owl")
RDF_PATH_BA = os.path.join(ROOT_DIR, "../data/buenos_aires_wifi.rdf")
RDF_PATH_NY = os.path.join(ROOT_DIR, "../data/FINAL CON INDIIVDUOS NY.rdf")
CONSULTAS_DIR = os.path.join(ROOT_DIR, "consultas")
PUBLIC_DIR = os.path.join(ROOT_DIR, "../public")

# --- Cargar ontologías ---
print(f"[INFO] Cargando ontologías y RDFs...")

g_ba = Graph()
g_ba.parse(ONTOLOGY_PATH_BA, format="xml")
try:
    with open(RDF_PATH_BA, "r", encoding="utf-8") as f:
        g_ba.parse(f, format="xml")
    print("[INFO] RDF de Buenos Aires cargado.")
except FileNotFoundError:
    print(f"[ERROR] RDF_PATH_BA no encontrado: {RDF_PATH_BA}")

g_ny = Graph()
g_ny.parse(ONTOLOGY_PATH_NY, format="xml")
try:
    with open(RDF_PATH_NY, "r", encoding="utf-8") as f:
        g_ny.parse(f, format="xml")
    print("[INFO] RDF de New York cargado.")
except FileNotFoundError:
    print(f"[ERROR] RDF_PATH_NY no encontrado: {RDF_PATH_NY}")

# --- API REST para visualización por ciudad y filtro ---
@app.get("/api/puntos")
def puntos(ciudad: str, consulta: str | None = None):
    puntos = []
    consulta_lower = consulta.lower() if consulta else None

    if "buenos" in ciudad.lower():
        g = g_ba
        WIFI = Namespace("http://example.org/wifi#")
        individuos = set(g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi)) | set(g.subjects(RDF.type, WIFI.WiFi))

        for punto in individuos:
            ssid = g.value(punto, WIFI.nombreSSID)
            lat = g.value(punto, WIFI.lat)
            lon = g.value(punto, WIFI.lon)
            estado = g.value(punto, WIFI.estado)
            proveedor = g.value(punto, WIFI.esOperadoPor)
            seguridad = g.value(punto, WIFI.usaSeguridad) or g.value(punto, WIFI.seguridad)

            if lat and lon:
                try:
                    lon_geo, lat_geo = transformer.transform(float(lon), float(lat))
                    punto_data = {
                        "ssid": str(ssid),
                        "lat": lat_geo,
                        "long": lon_geo,
                        "estado": str(estado) if estado else "",
                        "proveedor": str(proveedor) if proveedor else "",
                        "seguridad": str(seguridad) if seguridad else ""
                    }

                    if not consulta_lower or consulta_lower == "todos":
                        puntos.append(punto_data)
                    elif consulta_lower == "activos" and str(estado).lower() == "activo":
                        puntos.append(punto_data)
                    elif consulta_lower == "inactivos" and (not estado or str(estado).lower() != "activo"):
                        puntos.append(punto_data)
                    elif consulta_lower in {"abierto", "wpa2", "wpa3", "wep"} and seguridad and consulta_lower == str(seguridad).lower():
                        puntos.append(punto_data)
                    elif proveedor and consulta_lower in str(proveedor).lower():
                        puntos.append(punto_data)

                except Exception as e:
                    print(f"[WARN] Error de coordenadas en {ssid}: {e}")

    elif "new" in ciudad.lower():
        g = g_ny
        NYC = Namespace("http://example.org/nyc_wifi_nyc_public.owl#")

        for punto in g.subjects(RDF.type, None):
            ssid = g.value(punto, NYC.ssid)
            lat = g.value(punto, NYC.latitude)
            lon = g.value(punto, NYC.longitude)
            proveedor = g.value(punto, NYC.hasProvider)
            seguridad = None  # Seguridad no definida en NYC

            if lat and lon:
                try:
                    lon_geo, lat_geo = transformer.transform(float(lon), float(lat))
                    punto_data = {
                        "ssid": str(ssid),
                        "lat": lat_geo,
                        "long": lon_geo,
                        "proveedor": str(proveedor) if proveedor else "",
                        "seguridad": ""
                    }

                    if not consulta_lower or consulta_lower == "todos":
                        puntos.append(punto_data)
                    elif consulta_lower == "starbucks" and proveedor and "starbucks" in str(proveedor).lower():
                        puntos.append(punto_data)
                    elif proveedor and consulta_lower in str(proveedor).lower():
                        puntos.append(punto_data)
                    elif consulta_lower in {"abierto", "wpa2", "wpa3", "wep"} and seguridad and consulta_lower == str(seguridad).lower():
                        puntos.append(punto_data)

                except Exception as e:
                    print(f"[WARN] Error de coordenadas en {ssid}: {e}")
    else:
        raise HTTPException(status_code=400, detail="Ciudad no reconocida")

    return JSONResponse(content=puntos)

# --- API para ejecutar consultas SPARQL desde archivos .rq ---
@app.get("/api/sparql/{archivo}")
def ejecutar_sparql(archivo: str):
    ruta = os.path.join(CONSULTAS_DIR, f"{archivo}.rq")
    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    consulta = open(ruta, "r", encoding="utf-8").read()
    archivo_lower = archivo.lower()
    if "buenosaires" in archivo_lower or "_ba" in archivo_lower:
        grafo = g_ba
    elif "newyork" in archivo_lower or "_ny" in archivo_lower:
        grafo = g_ny
    else:
        grafo = g_ba + g_ny

    try:
        resultados = grafo.query(consulta)
        salida = [{str(var): str(row[var]) for var in row.labels} for row in resultados]
        return JSONResponse(content=salida)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar SPARQL: {str(e)}")

# --- Listado de archivos SPARQL disponibles ---
@app.get("/api/sparql/list")
def listar_consultas():
    archivos = [f.replace(".rq", "") for f in os.listdir(CONSULTAS_DIR) if f.endswith(".rq")]
    return JSONResponse(content=archivos)

# --- Montar frontend estático ---
app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")
