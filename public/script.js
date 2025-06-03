document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("filterForm");
    const map = L.map("map").setView([0, 0], 2);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    let markersLayer = L.layerGroup().addTo(map);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const city = form.city.value;
        const type = form.type.value;
        const coverage = form.coverage.value;

        const url = new URL("http://127.0.0.1:8000/api/wifi");
        url.searchParams.append("city", city);
        if (type) url.searchParams.append("type", type);
        if (coverage) url.searchParams.append("coverage", coverage);

        try {
            const res = await fetch(url);
            const data = await res.json();
            markersLayer.clearLayers();

            if (Array.isArray(data)) {
                data.forEach(p => {
                    if (p.lat && p.lon) {
                        L.marker([p.lat, p.lon])
                            .addTo(markersLayer)
                            .bindPopup(`<strong>${p.nombre}</strong><br>${p.direccion || ""}<br><em>${p.cobertura || ""}</em>`);
                    }
                });
                if (data.length > 0) {
                    map.setView([data[0].lat, data[0].lon], 13);
                }
            } else {
                alert("No se encontraron datos.");
            }
        } catch (err) {
            console.error("Error:", err);
            alert("Fallo al recuperar datos.");
        }
    });

    // Funciones de botones personalizados
    async function fetchWiFiAll() {
        const res = await fetch("/api/wifi/all");
        const data = await res.json();
        drawOnMap(data);
    }

    async function fetchWiFiByCity() {
        const city = prompt("Introduce el nombre de la ciudad:");
        const res = await fetch(`/api/wifi/city/${city}`);
        const data = await res.json();
        drawOnMap(data);
    }

    async function fetchWiFiByProvider() {
        const provider = prompt("Introduce el nombre del proveedor:");
        const res = await fetch(`/api/wifi/provider/${provider}`);
        const data = await res.json();
        drawOnMap(data);
    }

    async function fetchSecureWiFi() {
        const res = await fetch("/api/wifi/secure");
        const data = await res.json();
        drawOnMap(data);
    }

    async function fetchOpenWiFi() {
        const res = await fetch("/api/wifi/open");
        const data = await res.json();
        drawOnMap(data);
    }

    async function fetchConnectedDevices() {
        const res = await fetch("/api/wifi/devices");
        const data = await res.json();
        drawOnMap(data);
    }

    function drawOnMap(data) {
        markersLayer.clearLayers();
        const markers = data.map(item => 
            L.marker([item.latitude, item.longitude]).bindPopup(item.name || "Punto WiFi")
        );
        markers.forEach(marker => marker.addTo(markersLayer));
    }

    // Opcional: llamar a algún fetch inicial
    // fetchWiFiAll();
});
