from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rdflib import Graph
import rdflib
import os

app = FastAPI()

# CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "../data")
CONSULTAS_DIR = os.path.join(ROOT_DIR, "../consultas")
PUBLIC_DIR = os.path.join(ROOT_DIR, "../public")

# Diccionario: ciudad -> fichero OWL
OWL_FILES = {
    "Buenos Aires": os.path.join(DATA_DIR, "buenos_aires_wifi.owl"),
    "New York": os.path.join(DATA_DIR, "nyc_wifi_public.owl"),
}

def cargar_consulta(filename, params):
    with open(os.path.join(CONSULTAS_DIR, filename), "r", encoding="utf-8") as f:
        query = f.read()
    for key, value in params.items():
        query = query.replace(f"${key.upper()}", value)
    return query

def cargar_grafo_owl(ciudad):
    path = OWL_FILES.get(ciudad)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"No hay datos OWL para la ciudad '{ciudad}'.")
    g = Graph()
    g.parse(path, format="xml")
    return g

@app.get("/api/puntos")
def puntos(
    ciudad: str = Query(None),
    estado: str = Query(None),
    proveedor: str = Query(None),
    tipo: str = Query(None),
    seguridad: str = Query(None),
    barrio: str = Query(None)
):
    if not ciudad:
        raise HTTPException(status_code=400, detail="Debes especificar una ciudad.")

    g = cargar_grafo_owl(ciudad)

    # --- Detección de consulta según los parámetros recibidos ---
    # Orden de prioridad: barrio>estado>proveedor>seguridad>tipo>ciudad (solo)
    consulta_file = None
    params = {}

    if ciudad and barrio:
        consulta_file = "consulta_por_barrio_ciudad.rq"
        params = {"ciudad": ciudad, "barrio": barrio}
    elif estado:
        consulta_file = "consulta_por_estado.rq"
        params = {"estado": estado}
    elif proveedor:
        consulta_file = "consulta_por_proveedor.rq"
        params = {"proveedor": proveedor}
    elif seguridad:
        consulta_file = "consulta_por_seguridad.rq"
        params = {"seguridad": seguridad}
    elif tipo:
        consulta_file = "consulta_por_tipo_de_red.rq"
        params = {"tipo": tipo}
    elif ciudad:
        consulta_file = "consulta_por_ciudad.rq"
        params = {"ciudad": ciudad}
    else:
        raise HTTPException(status_code=400, detail="No hay parámetros de filtro suficientes.")

    # --- Ejecutar consulta ---
    sparql = cargar_consulta(consulta_file, params)
    try:
        results = g.query(sparql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar consulta SPARQL: {e}")

    puntos = []
    for row in results:
        punto = {str(k): (str(getattr(row, k)) if getattr(row, k) is not None else "") for k in row.labels}
        if "latitud" in punto: punto["lat"] = float(punto["latitud"])
        if "longitud" in punto: punto["long"] = float(punto["longitud"])
        puntos.append(punto)

    return JSONResponse(content=puntos)

# 🚀 NUEVO ENDPOINT: Comparar ciudades por número de puntos WiFi
@app.get("/api/comparar_ciudades")
async def comparar_ciudades():
    resultados_comparacion = []
    ciudades = ["Buenos Aires", "New York"]

    for ciudad in ciudades:
        g = cargar_grafo_owl(ciudad)
        query = cargar_consulta("consulta_comparar_ciudades.rq", {})  # sin parámetros
        results = g.query(query)

        for row in results:
            ciudad_nombre = str(row[0])
            total = int(row[1]) if row and row[1] else 0
            resultados_comparacion.append({
                "ciudad": ciudad_nombre,
                "total": total
            })

    return JSONResponse(content=resultados_comparacion)
# 🧩 FIN DEL NUEVO ENDPOINT

# Servir archivos estáticos (frontend)
app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")

@app.get("/api/valores")
def obtener_valores(filtro: str = Query(...), ciudad: str = Query(...)):
    archivo_consulta = f"consulta_{'proveedores_por_ciudad' if filtro == 'proveedor' else f'por_{filtro}'}.rq"

    g = cargar_grafo_owl(ciudad)
    try:
        sparql = cargar_consulta(archivo_consulta, {"ciudad": ciudad})
        resultados = g.query(sparql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta SPARQL: {e}")

    valores = sorted({str(row[0]) for row in resultados})
    return JSONResponse(content=valores)