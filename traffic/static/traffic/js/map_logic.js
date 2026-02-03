let map;
let userMarker;
let simulatedMarkers = [];
let routingControl;

function initMap() {
    // Initial position (Dakar as a default for African city context)
    const defaultPos = [14.7167, -17.4677];
    map = L.map('map').setView(defaultPos, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Try to get user position
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const pos = [position.coords.latitude, position.coords.longitude];
            map.setView(pos, 15);
            userMarker = L.marker(pos, {
                icon: L.icon({
                    iconUrl: 'https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png',
                    iconSize: [40, 40],
                    iconAnchor: [20, 40]
                })
            }).addTo(map).bindPopup("Vous êtes ici").openPopup();
            
            simulateNearbyUsers(pos);
        });
    }

    map.on('click', function(e) {
        if (routingControl) {
            map.removeControl(routingControl);
        }

        const start = userMarker ? userMarker.getLatLng() : defaultPos;
        const end = e.latlng;

        routingControl = L.Routing.control({
            waypoints: [
                L.latLng(start),
                L.latLng(end)
            ],
            routeWhileDragging: true,
            lineOptions: {
                styles: [{ color: '#38bdf8', opacity: 0.8, weight: 6 }]
            },
            createMarker: function() { return null; }
        }).addTo(map);
        
        // Update destination info in UI if needed
        updateRouteInfo(start, end);
    });
}

function simulateNearbyUsers(centerPos) {
    // Clear old markers
    simulatedMarkers.forEach(m => map.removeLayer(m));
    simulatedMarkers = [];

    for (let i = 0; i < 10; i++) {
        const lat = centerPos[0] + (Math.random() - 0.5) * 0.02;
        const lng = centerPos[1] + (Math.random() - 0.5) * 0.02;
        
        const marker = L.circleMarker([lat, lng], {
            radius: 8,
            fillColor: "#ef4444",
            color: "#fff",
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);
        
        simulatedMarkers.push(marker);
    }
}

function updateRouteInfo(start, end) {
    // Placeholder for distance calculation or additional UI feedback
    console.log("Calcul d'itinéraire...");
}

document.addEventListener('DOMContentLoaded', initMap);
