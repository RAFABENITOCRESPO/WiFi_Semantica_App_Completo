# 🌐 Proyecto Web Semántica - Visualización de Puntos WiFi

Este proyecto permite visualizar puntos públicos de acceso WiFi utilizando tecnologías de Web Semántica, RDF y SPARQL, con una API funcional en FastAPI y una interfaz de usuario basada en HTML y Leaflet.

---

## 📁 Estructura del Proyecto

```
WiFi_Semantica_App_Completo/
├── api/                       # Código backend (FastAPI)
├── backend/
│   ├── ontology/              # RDF y CSV por ciudad
│   └── queries/               # Consultas SPARQL
├── public/                   # Frontend HTML + Leaflet
├── data/                     # Datos RDF externos
├── instalador.bat            # Script Windows de instalación
├── lanzar_api.bat            # Ejecutar API
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
├── WIFI_SEMANTICA_PROYECTO_INFO_FINAL.md
```

---

## 🚀 Instalación

### Opción rápida (Windows):
Ejecuta `instalador.bat`.

### Opción manual:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Abre tu navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔗 Endpoints API

| Ciudad         | URL de Ejemplo                                |
|----------------|-----------------------------------------------|
| Nueva York     | `/api/wifi?city=New York`                     |
| Buenos Aires   | `/api/wifi?city=Buenos Aires`                 |

---

## 🧠 Ontología del Proyecto

### Clases Principales:
- `PuntoDeAccesoWiFi`
- `Ubicación`
- `Proveedor`
- `Seguridad`
- `Dispositivo`

### Ejemplo SPARQL:
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

## 📸 Interfaz

Visualiza los puntos WiFi directamente desde el archivo HTML en `public/index.html`, conectando con la API y usando Leaflet.js para mapas interactivos.

---

## 👤 Autor

Rafael Benito  
TFG – Universitat Oberta de Catalunya  
2025

---

## 📄 Licencia

MIT License