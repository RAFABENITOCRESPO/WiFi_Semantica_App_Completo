import csv
import json
import os
from datetime import datetime
from rdflib import Graph

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_csv(datos):
    filename = f"{EXPORT_DIR}/datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)
    return filename

def exportar_json(datos):
    filename = f"{EXPORT_DIR}/datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, mode="w", encoding='utf-8') as file:
        json.dump(datos, file, indent=4, ensure_ascii=False)
    return filename
def obtener_datos_exportar():
    g = Graph()
    # Cargar todos los ficheros OWL desde el directorio 'data'
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".owl"):
            g.parse(os.path.join(data_dir, filename), format="xml")

    query = """
    PREFIX ex: <http://example.org/wifi#>
    SELECT ?ssid ?ciudad ?barrio ?latitud ?longitud
    WHERE {
        ?punto a ex:PuntoDeAccesoWiFi ;
               ex:ssid ?ssid ;
               ex:ciudad ?ciudad ;
               ex:barrio ?barrio ;
               ex:latitud ?latitud ;
               ex:longitud ?longitud .
    }
    """

    resultados = g.query(query)
    datos = []

    for row in resultados:
        datos.append({
            "ssid": str(row.ssid),
            "ciudad": str(row.ciudad),
            "barrio": str(row.barrio),
            "latitud": str(row.latitud),
            "longitud": str(row.longitud)
        })

    return datos