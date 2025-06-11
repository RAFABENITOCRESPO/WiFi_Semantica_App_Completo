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
-`.gitignore`, `README.md`: documentación y configuración
## Nuevas consultas

Se añadió una ontología extendida con clases de puntos de acceso, ubicaciones, proveedores, dispositivos y protocolos de seguridad. La API ahora incluye los siguientes endpoints adicionales:

- `/api/consulta/streaming` – devuelve los puntos con `aptoParaStreaming` verdadero.
- `/api/consulta/seguridad_debil` – lista los accesos con seguridad débil (WEP).
- `/api/consulta/tiempo_completo` – muestra los accesos disponibles las 24 horas.

La ontología extendida se encuentra en `data/wifi_ontology_extended.owl`.