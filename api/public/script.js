
async function cargarDatos(ciudad, consulta) {
    try {
        const response = await fetch(`/api/consulta?ciudad=${encodeURIComponent(ciudad)}&consulta=${consulta}`);
        const data = await response.json();

        if (Array.isArray(data)) {
            agregarPuntosAlMapa(data);
        } else {
            console.warn("Datos no válidos recibidos:", data);
        }
    } catch (error) {
        console.error("Error al cargar datos:", error);
    }
}

function agregarPuntosAlMapa(data) {
    if (window.markersLayer) {
        window.markersLayer.clearLayers();
    } else {
        window.markersLayer = L.layerGroup().addTo(map);
    }

    data.forEach(punto => {
        if (punto.lat && punto.lon) {
            const marker = L.marker([punto.lat, punto.lon])
                .bindPopup(`<b>${punto.nombre}</b><br>${punto.direccion}`);
            window.markersLayer.addLayer(marker);
        }
    });
}
