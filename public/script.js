
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
            renderChartComparacion(datos);
        } else {
            alert("❌ No se pudo obtener la comparación de ciudades.");
        }
    } catch (e) {
        console.error("Error al comparar ciudades:", e);
        alert("⚠️ Ocurrió un error al intentar comparar las ciudades.");
    }
});

let chartEstadisticas, chartComparacion;

function renderChartEstadisticas(data, ciudad) {
    const ctx = document.getElementById("chartEstadisticas").getContext("2d");
    if (chartEstadisticas) chartEstadisticas.destroy();
    chartEstadisticas = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Proveedores", "Tipos", "Seguridad", "Barrios"],
            datasets: [{
                label: `Conteo de categorías en ${ciudad}`,
                data: [
                    data.proveedores.length,
                    data.tipos.length,
                    data.seguridad.length,
                    data.barrios.length
                ],
                backgroundColor: ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2"]
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

function renderChartComparacion(ciudades) {
    const ctx = document.getElementById("chartComparacion").getContext("2d");
    if (chartComparacion) chartComparacion.destroy();
    chartComparacion = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ciudades.map(c => c.ciudad),
            datasets: [{
                label: "Puntos WiFi por ciudad",
                data: ciudades.map(c => c.total),
                backgroundColor: ["#59a14f", "#edc948"]
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}
document.getElementById("btnExportarJSON").addEventListener("click", () => {
    fetch("/api/export/json")
        .then(response => {
            if (!response.ok) throw new Error("Error exportando JSON");
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "datos_exportados.json";
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => console.error("Error:", error));
});

document.getElementById("btnExportarCSV").addEventListener("click", () => {
    fetch("/api/export/csv")
        .then(response => {
            if (!response.ok) throw new Error("Error exportando CSV");
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "datos_exportados.csv";
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => console.error("Error:", error));
});
document.getElementById('btnEstadisticas').addEventListener('click', () => {
    const ciudad = document.getElementById('ciudad').value;
    if (!ciudad) return alert("Selecciona una ciudad para ver las estadísticas.");
    fetch(`/api/estadisticas/${encodeURIComponent(ciudad)}`)
        .then(response => {
            if (!response.ok) throw new Error("Error al obtener estadísticas");
            return response.json();
        })
        .then(data => {
            const resumen = `
Estadísticas de ${ciudad}:
- Total de puntos: ${data.total}
- Proveedores: ${data.proveedores.join(', ')}
- Tipos: ${data.tipos.join(', ')}
- Niveles de seguridad: ${data.seguridad.join(', ')}
- Barrios: ${data.barrios.join(', ')}
            `;
            renderChartEstadisticas(data, ciudad);
        })
        .catch(err => {
            console.error(err);
            alert("No se pudieron cargar las estadísticas.");
        });
});


document.getElementById("btnExportarPDF").addEventListener("click", () => {
    const chartArea = document.getElementById("chartEstadisticas").parentElement;
    html2canvas(chartArea).then(canvas => {
        const imgData = canvas.toDataURL("image/png");
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF();
        pdf.addImage(imgData, 'PNG', 10, 10, 190, 100);
        pdf.save("estadisticas_wifi.pdf");
    });
});


document.getElementById("btnRecomendacion").addEventListener("click", () => {
    const ciudad = document.getElementById("ciudad").value;
    fetch(`/api/estadisticas/${ciudad}`)
        .then(res => res.json())
        .then(data => {
            let mejor = "";
            let max = 0;
            const conteos = {};
            data.barrios.forEach(b => {
                conteos[b] = (conteos[b] || 0) + 1;
                if (conteos[b] > max) {
                    max = conteos[b];
                    mejor = b;
                }
            });
            const msg = mejor ? `📍 Mejor zona en ${ciudad}: ${mejor} (con ${max} puntos WiFi)` : "No hay datos suficientes.";
            document.getElementById("recomendacion").textContent = msg;
        });
});
