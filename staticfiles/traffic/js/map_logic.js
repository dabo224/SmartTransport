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
    const geoOptions = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const pos = [position.coords.latitude, position.coords.longitude];
            map.setView(pos, 15);

            userMarker = L.marker(pos, {
                draggable: true,
                icon: L.icon({
                    iconUrl: 'https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png',
                    iconSize: [40, 40],
                    iconAnchor: [20, 40]
                })
            }).addTo(map).bindPopup("Vous êtes ici (Déplacez-moi si besoin)").openPopup();

            userMarker.on('dragend', function (event) {
                const marker = event.target;
                const position = marker.getLatLng();
                marker.setLatLng(new L.LatLng(position.lat, position.lng));
                console.log("Nouvelle position manuelle :", position);

                // If a route exists, update it
                if (routingControl) {
                    const waypoints = routingControl.getWaypoints();
                    routingControl.setWaypoints([
                        L.latLng(position.lat, position.lng),
                        waypoints[1].latLng
                    ]);
                }
            });

            simulateNearbyUsers(pos);
        }, error => {
            console.warn(`ERROR(${error.code}): ${error.message}`);
            // Fallback to default position if error
            simulateNearbyUsers(defaultPos);
        }, geoOptions);
    }

    map.on('click', function (e) {
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
            position: 'topright',
            lineOptions: {
                styles: [{ color: '#38bdf8', opacity: 0.8, weight: 6 }]
            },
            createMarker: function () { return null; }
        }).addTo(map);

        // Update destination info in UI if needed
        updateRouteInfo(start, end);
    });
}

function simulateNearbyUsers(centerPos) {
    // Clear old markers
    simulatedMarkers.forEach(item => map.removeLayer(item.marker));
    simulatedMarkers = [];

    const routingService = L.Routing.osrmv1({
        serviceUrl: 'https://router.project-osrm.org/route/v1'
    });

    for (let i = 0; i < 8; i++) { // Reduced count to be polite to the API
        const startLat = centerPos[0] + (Math.random() - 0.5) * 0.01;
        const startLng = centerPos[1] + (Math.random() - 0.5) * 0.01;
        const endLat = centerPos[0] + (Math.random() - 0.5) * 0.02;
        const endLng = centerPos[1] + (Math.random() - 0.5) * 0.02;

        const marker = L.circleMarker([startLat, startLng], {
            radius: 6,
            fillColor: "#ef4444",
            color: "#fff",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.9
        }).addTo(map);

        const simItem = {
            marker: marker,
            path: [],
            pathIndex: 0,
            centerPos: centerPos
        };
        simulatedMarkers.push(simItem);
        fetchNewRoute(simItem, routingService);
    }

    if (!window.animationStarted) {
        animateMarkers();
        window.animationStarted = true;
    }
}

function fetchNewRoute(simItem, service) {
    const start = simItem.marker.getLatLng();
    const endLat = simItem.centerPos[0] + (Math.random() - 0.5) * 0.02;
    const endLng = simItem.centerPos[1] + (Math.random() - 0.5) * 0.02;

    service.route([
        { latLng: L.latLng(start.lat, start.lng) },
        { latLng: L.latLng(endLat, endLng) }
    ], (err, routes) => {
        if (!err && routes && routes[0]) {
            simItem.path = routes[0].coordinates;
            simItem.pathIndex = 0;
        } else {
            // Retry later if failed
            setTimeout(() => fetchNewRoute(simItem, service), 5000);
        }
    });
}

function animateMarkers() {
    simulatedMarkers.forEach(simItem => {
        if (simItem.path && simItem.path.length > 0 && simItem.pathIndex < simItem.path.length) {
            const nextCoord = simItem.path[simItem.pathIndex];
            simItem.marker.setLatLng([nextCoord.lat, nextCoord.lng]);
            simItem.pathIndex++;

            if (simItem.pathIndex >= simItem.path.length) {
                // Reached destination, get new route
                const routingService = L.Routing.osrmv1({
                    serviceUrl: 'https://router.project-osrm.org/route/v1'
                });
                fetchNewRoute(simItem, routingService);
            }
        }
    });

    // Slow down the animation a bit for realism (approx 10-15 fps for traffic feel)
    setTimeout(() => {
        requestAnimationFrame(animateMarkers);
    }, 100);
}

function updateRouteInfo(start, end) {
    // Placeholder for distance calculation or additional UI feedback
    console.log("Calcul d'itinéraire...");
}

document.addEventListener('DOMContentLoaded', initMap);
