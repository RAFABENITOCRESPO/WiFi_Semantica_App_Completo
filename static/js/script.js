document.addEventListener("DOMContentLoaded", () => {
    const map = L.map("map").setView([40.4168, -3.7038], 3);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    }).addTo(map);

    const buttons = {
        todos: "/api/consulta/wifi",
        ciudad: "/api/consulta/por_ciudad?city=New York",
        proveedor: "/api/consulta/por_proveedor?proveedor=Movistar",
        seguros: "/api/consulta/seguro",
        abiertos: "/api/consulta/abierto",
        dispositivos: "/api/consulta/dispositivos"
    };

    const addMarkers = (data) => {
        map.eachLayer((layer) => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        data.forEach((item) => {
            const lat = parseFloat(item.lat);
            const lon = parseFloat(item.lon);
            if (!isNaN(lat) && !isNaN(lon)) {
                L.marker([lat, lon])
                    .addTo(map)
                    .bindPopup(`<strong>${item.nombre}</strong><br>Proveedor: ${item.proveedor || "N/A"}<br>Seguridad: ${item.seguridad || "N/A"}`);
            }
        });
    };

    const fetchData = (endpoint) => {
        fetch(endpoint)
            .then((res) => {
                if (!res.ok) throw new Error("Error al cargar los datos");
                return res.json();
            })
            .then((data) => addMarkers(data))
            .catch((err) => console.error("Error:", err));
    };

    document.getElementById("btn-todos").addEventListener("click", () => fetchData(buttons.todos));
    document.getElementById("btn-ciudad").addEventListener("click", () => fetchData(buttons.ciudad));
    document.getElementById("btn-proveedor").addEventListener("click", () => fetchData(buttons.proveedor));
    document.getElementById("btn-seguros").addEventListener("click", () => fetchData(buttons.seguros));
    document.getElementById("btn-abiertos").addEventListener("click", () => fetchData(buttons.abiertos));
    document.getElementById("btn-dispositivos").addEventListener("click", () => fetchData(buttons.dispositivos));
});