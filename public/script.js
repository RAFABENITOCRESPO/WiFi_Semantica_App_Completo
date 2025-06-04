let map = L.map('map').setView([-34.61, -58.38], 12); // Vista inicial en Buenos Aires

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

const ciudadSelect = document.getElementById('city');

function limpiarMarcadores() {
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });
}

function cargarDatos(tipo = '') {
    const ciudad = ciudadSelect.value;
    let endpoint = '';

    switch (tipo) {
        case 'general':
            endpoint = '/api/consulta/wifi';
            break;
        case 'por_ciudad':
            endpoint = '/api/consulta/por_ciudad';
            break;
        case 'por_proveedor':
            endpoint = '/api/consulta/por_proveedor';
            break;
        case 'abierto':
            endpoint = '/api/consulta/abierto';
            break;
        case 'seguro':
            endpoint = '/api/consulta/seguro';
            break;
        case 'dispositivos':
            endpoint = '/api/consulta/dispositivos';
            break;
        default:
            endpoint = '/api/wifi?city=' + encodeURIComponent(ciudad);
    }

    fetch('http://127.0.0.1:8000' + endpoint)
        .then(res => {
            if (!res.ok) {
                throw new Error('Respuesta de red no OK');
            }
            return res.json();
        })
        .then(data => {
            limpiarMarcadores();
            if (data.length > 0) {
                map.setView([data[0].lat, data[0].lon], 13);
            }
            data.forEach(punto => {
                if (punto.lat && punto.lon) {
                    const marker = L.marker([punto.lat, punto.lon]).addTo(map);
                    const texto = punto.proveedor || punto.nombre || "WiFi";
                    marker.bindPopup(`${texto}<br>${punto.ciudad || punto.direccion || ''}`);
                }
            });
        })
        .catch(err => {
            console.error('Error al obtener datos:', err);
            alert("No se pudieron cargar los datos. Verifica que la API esté funcionando.");
        });
}

ciudadSelect.addEventListener('change', () => {
    cargarDatos(); // Llamada sin tipo para consulta por ciudad
});

// Carga inicial
cargarDatos();