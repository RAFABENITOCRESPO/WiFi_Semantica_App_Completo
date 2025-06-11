# WiFi Semántica App (Versión Avanzada)

Una aplicación que permite la consulta, visualización, análisis y exportación de datos sobre puntos de acceso WiFi utilizando RDF y datos abiertos.

## Funciones clave:

- 🔍 Búsqueda por ciudad, tipo o cobertura
- 🗺️ Mapa interactivo (Leaflet)
- 🧩 Filtros avanzados por proveedor, velocidad o área
- 📊 Estadísticas básicas de conectividad por zona
- ⚖️ Comparación entre ciudades
- 📡 Preparado para integrarse con endpoints SPARQL

## Estructura del proyecto

- `index.html`: interfaz visual con Leaflet + filtros
- `api/export_tools.py`: exportación de resultados
- `api/statistics_tools.py`: estadísticas de uso
- `data/`: RDF, CSV, GeoJSON y fuentes de datos
-`.gitignore`, `README.md`: documentación y configuración
## Nuevas consultas

La ontología integra clases de puntos de acceso, ubicaciones, proveedores,
dispositivos y protocolos de seguridad. dispositivos y protocolos de seguridad. 

Los ejemplos de consultas SPARQL se
encuentran en el directorio `backend/queries` y se pueden ejecutar desde la API
con el endpoint `/api/run_query`:

```bash
curl "http://localhost:8000/api/run_query?name=consulta_abiertos_buenosaires"
```

La ontología utilizada se encuentra en `data/ontology.owl`.

