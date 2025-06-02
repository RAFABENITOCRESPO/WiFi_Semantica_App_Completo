# WiFi Semántica App (Versión Avanzada)

Una aplicación que permite la consulta, visualización, análisis y exportación de datos sobre puntos de acceso WiFi utilizando RDF y datos abiertos.

## Funciones clave:

- 🔍 Búsqueda por ciudad, tipo o cobertura
- 🗺️ Mapa interactivo (Leaflet)
- 🧩 Filtros avanzados por proveedor, velocidad o área
- 📊 Estadísticas básicas de conectividad por zona
- ⚖️ Comparación entre ciudades
- 💾 Exportación en CSV y JSON
- 📡 Preparado para integrarse con endpoints SPARQL

## Estructura del proyecto

- `public/index.html`: interfaz visual con Leaflet + filtros
- `api/export_tools.py`: exportación de resultados
- `api/statistics_tools.py`: estadísticas de uso
- `data/`: RDF, CSV, GeoJSON y fuentes de datos
- `.gitignore`, `README.md`: documentación y configuración