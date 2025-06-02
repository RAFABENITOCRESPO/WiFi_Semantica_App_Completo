from flask import Flask, jsonify
from rdflib import Graph

app = Flask(__name__)

@app.route('/api/wifi')
def consultar_wifi():
    g = Graph()
    g.parse("backend/ontology/wifi_ny.rdf", format="xml")

    q = """
    PREFIX ex: <http://example.org/wifi#>
    SELECT ?nombre ?latitud ?longitud WHERE {
      ?punto a ex:PuntoDeAccesoWiFi ;
             ex:nombre ?nombre ;
             ex:latitud ?latitud ;
             ex:longitud ?longitud .
    }
    """

    results = g.query(q)
    puntos = []
    for row in results:
        puntos.append({
            "nombre": str(row.nombre),
            "latitud": float(row.latitud),
            "longitud": float(row.longitud)
        })

    return jsonify(puntos)

if __name__ == '__main__':
    app.run(debug=True)