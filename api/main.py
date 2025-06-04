from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import pandas as pd
from rdflib import Graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ontología combinada con los puntos WiFi de ambas ciudades
BASE_ONTOLOGY_PATH = "data/wifi_ontology_combined.owl"
QUERY_PATH = "backend/queries/"

def execute_query(file_name: str):
    g = Graph()
    g.parse(BASE_ONTOLOGY_PATH)
    with open(f"{QUERY_PATH}{file_name}", "r", encoding="utf-8") as f:
        query = f.read()
    results = g.query(query)
    return [{str(var): str(row[var]) for var in row.labels} for row in results]

@app.get("/api/consulta/wifi")
def consulta_general():
    return execute_query("consulta_wifi.rq")

@app.get("/api/consulta/por_ciudad")
def consulta_por_ciudad():
    return execute_query("wifi_por_ciudad.rq")

@app.get("/api/consulta/por_proveedor")
def consulta_por_proveedor():
    return execute_query("wifi_por_proveedor.rq")

@app.get("/api/consulta/seguro")
def consulta_wifi_seguro():
    return execute_query("wifi_seguro.rq")

@app.get("/api/consulta/abierto")
def consulta_wifi_abierto():
    return execute_query("wifi_abierto.rq")

@app.get("/api/consulta/dispositivos")
def consulta_dispositivos_por_wifi():
    return execute_query("dispositivos_por_wifi.rq")

@app.get("/api/wifi")
def get_wifi_points(city: str = Query(..., description="Nombre de la ciudad (ej. New York o Buenos Aires)")):
    city_clean = city.strip().lower()

    if city_clean == "new york":
        g = Graph()
        g.parse("data/FINAL_CON_INDIIVDUOS_NY.rdf")
        query = """
        SELECT ?nombre ?direccion ?lat ?lon WHERE {
            ?s <http://schema.org/name> ?nombre .
            ?s <http://schema.org/address> ?direccion .
            ?s <http://schema.org/latitude> ?lat .
            ?s <http://schema.org/longitude> ?lon .
        }
        """
        results = g.query(query)
        data = [
            {
                "nombre": str(row.nombre),
                "direccion": str(row.direccion),
                "lat": float(row.lat),
                "lon": float(row.lon)
            }
            for row in results
        ]
        return data

    elif city_clean == "buenos aires":
        df = pd.read_csv("data/puntos_wifi_ba.csv")
        return df.to_dict(orient="records")

    else:
        return {"error": "Ciudad no encontrada"}