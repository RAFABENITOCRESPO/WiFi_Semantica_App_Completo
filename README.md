# 📡 WiFi Semántica App

Una aplicación web interactiva que permite consultar, visualizar, analizar y exportar datos sobre puntos de acceso WiFi utilizando tecnologías semánticas (OWL, RDF, SPARQL) y datos abiertos de ciudades como Buenos Aires y Nueva York.

---

## 🚀 Funcionalidades Clave

- 🔍 **Búsqueda por ciudad, tipo, proveedor, estado, barrio y seguridad.**
- 🧩 **Filtros avanzados combinados** para una búsqueda más precisa.
- 🗺️ **Mapa interactivo con Leaflet** mostrando los puntos WiFi según los filtros aplicados.
- 🧮 **Consultas SPARQL** automáticas en función del filtro seleccionado.
- 📊 **Estadísticas visuales** (gráficos dinámicos por proveedor, tipo, seguridad, barrio...).
- ⚖️ **Comparativas entre ciudades** con representación gráfica.
- 📤 **Exportación de resultados** en formatos: CSV, JSON y PDF.
- 🤖 **Recomendación automática** de la mejor zona de cobertura WiFi por ciudad.
- 💬 **Interfaz fácil de usar** y preparada para ampliaciones futuras.

---

## 🧠 Tecnologías Utilizadas

- **Ontologías y Datos**: OWL, RDF, SPARQL, Protégé, OpenData (Buenos Aires y NYC)
- **Backend (API REST)**: Python, FastAPI, RDFlib
- **Frontend (UI)**: HTML, JavaScript, Leaflet, Chart.js
- **Exportación**: jsPDF, html2canvas

---

## 📁 Estructura del Proyecto

- `index.html` – Interfaz gráfica (mapa, filtros, botones, estadísticas)
- `public/script.js` – Lógica del frontend y conexión con la API
- `api/main.py` – Backend FastAPI con endpoints SPARQL y exportación
- `api/export_tools.py` – Generación de CSV y JSON
- `api/statistics_tools.py` – Generación de estadísticas por ciudad
- `data/` – RDF, OWL, y fuentes de datos (NY y BA)
- `api/consultas/` – SPARQL queries organizadas por tipo
- `README.md` – Documentación del proyecto

---

## 🧪 Ejemplo de Consultas SPARQL vía API

Puedes ejecutar cualquier consulta SPARQL desde el backend utilizando este endpoint:

```bash
curl "http://localhost:8000/api/run_query?name=consulta_activos_buenosaires"