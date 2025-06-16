from rdflib import Graph, Namespace, RDF
import os

# Ruta correcta basada en la estructura del proyecto
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "../data")

WIFI = Namespace("http://example.org/wifi#")

CIUDADES_OWL = {
    "Buenos Aires": os.path.join(DATA_DIR, "buenos_aires_wifi.owl"),
    "New York": os.path.join(DATA_DIR, "nyc_wifi_public.owl"),
}

def obtener_estadisticas(ciudad):
    path = CIUDADES_OWL.get(ciudad)
    if not path or not os.path.isfile(path):
        raise FileNotFoundError(f"No se encontró el archivo OWL para {ciudad}")

    g = Graph()
    g.parse(path, format="xml")

    total = len(list(g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi)))

    proveedores = set()
    tipos = set()
    seguridad = set()
    barrios = set()

    for s in g.subjects(RDF.type, WIFI.PuntoDeAccesoWiFi):
        for p in g.objects(s, WIFI.proveedor):
            proveedores.add(str(p))
        for t in g.objects(s, WIFI.tipo):
            tipos.add(str(t))
        for seg in g.objects(s, WIFI.seguridad):
            seguridad.add(str(seg))
        for b in g.objects(s, WIFI.barrio):
            barrios.add(str(b))

    return {
        "total": total,
        "proveedores": list(proveedores),
        "tipos": list(tipos),
        "seguridad": list(seguridad),
        "barrios": list(barrios),
    }
