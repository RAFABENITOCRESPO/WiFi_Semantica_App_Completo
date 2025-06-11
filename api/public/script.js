
async function cargarDatos(ciudad, consulta) {
    try {
        const response = await fetch(`/api/puntos?ciudad=${encodeURIComponent(ciudad)}`);
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
        if (punto.lat && punto.long) {
            const marker = L.marker([punto.lat, punto.long])
                .bindPopup(`<b>${punto.ssid}</b><br>${'Seguridad: ' + punto.seguridad + '<br>Proveedor: ' + punto.proveedor}`);
            window.markersLayer.addLayer(marker);
        }
    });
}
