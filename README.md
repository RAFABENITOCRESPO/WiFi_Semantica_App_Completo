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
dispositivos y protocolos de seguridad. Actualmente la API expone los
siguientes endpoints:

- `/api/consulta` – consulta general filtrando por ciudad y tipo.
- `/api/consulta/seguridad_debil` – lista los accesos con seguridad débil
  (WEP).

La ontología utilizada se encuentra en `data/ontology.owl`.