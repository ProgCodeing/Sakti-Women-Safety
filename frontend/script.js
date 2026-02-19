async function findRoute() {

    let start = document.getElementById("start").value;
    let end = document.getElementById("end").value;

    const startCoords = await getCoordinates(start);
    const endCoords = await getCoordinates(end);

    if (!startCoords || !endCoords) return;

    // Clear old map
    map.setView([startCoords.lat, startCoords.lon], 13);

    L.marker([startCoords.lat, startCoords.lon]).addTo(map)
        .bindPopup("Start").openPopup();

    L.marker([endCoords.lat, endCoords.lon]).addTo(map)
        .bindPopup("Destination");

    document.getElementById("result").innerHTML =
        `Route from ${start} to ${end} displayed on map.`;
}


async function getCoordinates(place) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(place)}`;

    const response = await fetch(url);
    const data = await response.json();

    if (data.length === 0) {
        alert("Location not found!");
        return null;
    }

    return {
        lat: parseFloat(data[0].lat),
        lon: parseFloat(data[0].lon)
    };
}
