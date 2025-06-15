
let map;
let markers = [];

function initMap() {
    map = L.map('map').setView([-34.60, -58.38], 12); // Default to BA
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © OpenStreetMap contributors'
    }).addTo(map);
}
initMap();

function clearMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

function mostrarResultados(puntos) {
    const tabla = document.getElementById('tablaResultados');
    const tbody = tabla.querySelector('tbody');
    tbody.innerHTML = '';
    if (!puntos || puntos.length === 0) {
        tabla.style.display = "none";
        return;
    }
    puntos.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${p.ssid || ''}</td><td>${p.ciudad || ''}</td><td>${p.barrio || ''}</td><td>${p.lat || ''}</td><td>${p.long || ''}</td>`;
        tbody.appendChild(tr);
    });
    tabla.style.display = "";
}

function centrarCiudad(ciudad) {
    if (ciudad === "New York") map.setView([40.75, -73.98], 12);
    else map.setView([-34.60, -58.38], 12);
}

const valoresPorFiltro = {
    estado: ["Disponible", "No Disponible"],
    proveedor: ["Gobierno BA", "Subterráneos BA", "LinkNYC", "Google Fiber", "Starbucks", "Municipalidad de NYC"],
    tipo: ["WiFi_Publico", "WiFi_Privado", "WiFi_municipal"],
    seguridad: ["Abierto", "WEP", "WPA", "WPA2", "WPA3"],
    barrio: {
        "Buenos Aires": ["Palermo", "Recoleta", "Caballito", "Belgrano", "Liniers", "Saavedra", "Villa Devoto", "San Telmo"],
        "New York": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
    }
};

document.getElementById('tipoConsulta').addEventListener('change', function () {
    const tipo = this.value;
    const ciudad = document.getElementById('ciudad').value;
    const sel = document.getElementById('valorFiltro');
    sel.innerHTML = '<option value="">-- Selecciona --</option>';
    if (!tipo) return;

    const valores = (tipo === 'barrio') ? valoresPorFiltro.barrio[ciudad] : valoresPorFiltro[tipo];
    valores.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        sel.appendChild(opt);
    });
});

document.getElementById('ciudad').addEventListener('change', function () {
    centrarCiudad(this.value);
    document.getElementById('tipoConsulta').dispatchEvent(new Event('change'));
});

document.getElementById('btnBuscar').addEventListener('click', async function () {
    const ciudad = document.getElementById('ciudad').value;
    const filtro = document.getElementById('tipoConsulta').value;
    const valor = document.getElementById('valorFiltro').value;

    let url = `/api/puntos?ciudad=${encodeURIComponent(ciudad)}`;
    if (filtro && valor) url += `&${filtro}=${encodeURIComponent(valor)}`;

    try {
        const resp = await fetch(url);
        if (resp.ok) {
            const puntos = await resp.json();
            clearMarkers();
            mostrarResultados(puntos);
            if (puntos && puntos.length > 0) {
                puntos.forEach(p => {
                    if (p.lat && p.long) {
                        const marker = L.marker([p.lat, p.long]).addTo(map)
                            .bindPopup(`<b>${p.ssid || ""}</b><br>${p.barrio || ""}`);
                        markers.push(marker);
                    }
                });
                map.setView([puntos[0].lat, puntos[0].long], 13);
            }
        } else {
            clearMarkers();
            mostrarResultados([]);
        }
    } catch (e) {
        clearMarkers();
        mostrarResultados([]);
    }
});
document.getElementById('btnComparar').addEventListener('click', async function () {
    try {
        const resp = await fetch('/api/comparar_ciudades');
        if (resp.ok) {
            const datos = await resp.json();
            let resultados = "📊 Comparativa de Ciudades:\n\n";
            datos.forEach(ciudad => {
                resultados += `🌍 ${ciudad.ciudad}: ${ciudad.total} puntos WiFi\n`;
            });
            alert(resultados);
        } else {
            alert("❌ No se pudo obtener la comparación de ciudades.");
        }
    } catch (e) {
        console.error("Error al comparar ciudades:", e);
        alert("⚠️ Ocurrió un error al intentar comparar las ciudades.");
    }
});