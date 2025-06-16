# utils.py
from rdflib import Graph

def load_graph(ciudad):
    g = Graph()
    if ciudad == "Buenos Aires":
        g.parse("data/buenos_aires_wifi.owl", format="xml")
    elif ciudad == "New York":
        g.parse("data/nyc_wifi_public.owl", format="xml")
    return g
