
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
