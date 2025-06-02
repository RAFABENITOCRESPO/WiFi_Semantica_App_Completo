# Proyecto WiFi Semántica - Documentación Técnica

## 📌 Nombre del Proyecto
Visualización de Puntos de Acceso WiFi mediante Web Semántica

## 🧠 Objetivo
Construir una aplicación funcional que permite consultar y visualizar puntos WiFi públicos usando datos estructurados en una ontología RDF, accesible mediante una API REST en Python.

## 📁 Estructura del Proyecto

- `/backend`: API REST (FastAPI) con RDFLib
- `/ontology`: RDF de puntos WiFi por ciudad (Buenos Aires, Nueva York)
- `/queries`: Consultas SPARQL para extracción semántica
- `/public`: Interfaz HTML con Leaflet.js y fetch
- `/data`: CSVs y archivos geográficos (GeoJSON) de entrada
- `README.md`: Documentación general
- `requirements.txt`: Dependencias
- `instalador.bat`: Instalador automático para Windows

## 🧰 Tecnologías Utilizadas

- **Lenguaje**: Python 3
- **Framework**: FastAPI
- **Ontologías**: RDF/XML + SPARQL
- **Frontend**: HTML5 + JavaScript + Leaflet.js
- **Visualización**: Mapas interactivos con puntos WiFi

## 🔍 Descripción Técnica

1. El backend lee archivos RDF y expone endpoints RESTful.
2. Se ejecutan consultas SPARQL para filtrar puntos WiFi por ciudad.
3. La API entrega los datos en formato JSON.
4. El frontend recibe los datos y muestra los puntos en el mapa según la ciudad seleccionada.

## 🛠️ Ejecución Local

### Requisitos:

- Python 3.10+
- pip

### Instalación automática (Windows):

```bat
instalador.bat
```

### Manual:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Abrir navegador en: http://127.0.0.1:8000

---

## 📬 Endpoints API

- `/api/wifi?city=New York`
- `/api/wifi?city=Buenos Aires`

---

## 🧪 SPARQL Ejemplo

```sparql
PREFIX ex: <http://example.org/wifi#>
SELECT ?nombre ?latitud ?longitud WHERE {
  ?p a ex:PuntoDeAccesoWiFi ;
     ex:nombre ?nombre ;
     ex:latitud ?latitud ;
     ex:longitud ?longitud .
}
```

---

## 🧩 Clases Principales de la Ontología

- **PuntoDeAccesoWiFi**
- **Ubicación**
- **Proveedor**
- **Seguridad**
- **Dispositivo**

---

## 👨‍💻 Autor
Rafael Benito – TFG Ingeniería Informática – Universitat Oberta de Catalunya