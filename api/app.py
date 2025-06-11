from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import os
from rdflib import Graph

app = FastAPI()

# Montar carpeta estática
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar ambos RDFs: NYC + Buenos Aires
graph = Graph()
graph.parse("wifi_data.rdf", format="xml")
graph.parse("wifi_ba.rdf", format="xml")  # nuevo grafo fusionado

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/wifi")
async def get_geojson(city: str = "nyc"):
    filename = f"wifi_{city}.geojson"
    filepath = os.path.join("static", filename)
    if not os.path.exists(filepath):
        return JSONResponse(content={"error": "Archivo no encontrado"}, status_code=404)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(content=data)

@app.get("/api/sparql")
async def sparql_query(q: str):
    try:
        results = []
        qres = graph.query(q)
        for row in qres:
            result = {f"var{i}": str(cell) for i, cell in enumerate(row)}
            results.append(result)
        return {"results": results}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
