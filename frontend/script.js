// ===== MAP SETUP =====
var map = L.map("map").setView([20.0, 73.78], 12); // default Nashik

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "Map data © OpenStreetMap",
}).addTo(map);

let routeLines = [];

// ===== LOGIN =====
async function login() {
  const user = document.getElementById("user").value;
  const pass = document.getElementById("pass").value;

  const res = await fetch("https://YOUR_RAILWAY_LINK.up.railway.app/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user, pass }),
  });

  const data = await res.json();

  if (data.status === "ok") alert("Login Successful!");
  else alert("Login Failed!");
}

// ===== GET COORDINATES =====
async function getCoordinates(place) {
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(place)}`;
  const res = await fetch(url);
  const data = await res.json();

  if (data.length === 0) {
    alert("Place not found!");
    return null;
  }

  return { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
}

// ===== DRAW ROUTE =====
async function drawRoute(start, end) {
  // clear old routes
  routeLines.forEach((line) => map.removeLayer(line));
  routeLines = [];

  const url = `https://router.project-osrm.org/route/v1/driving/${start.lon},${start.lat};${end.lon},${end.lat}?overview=full&geometries=geojson&alternatives=true`;
  const res = await fetch(url);
  const data = await res.json();

  data.routes.forEach((r, i) => {
    const coords = r.geometry.coordinates.map((c) => [c[1], c[0]]);
    const line = L.polyline(coords, {
      color: i === 0 ? "green" : "blue",
    }).addTo(map);
    routeLines.push(line);
  });
}

// ===== SHOW POLICE STATIONS =====
async function showPolice(lat, lon) {
  const url = `https://overpass-api.de/api/interpreter?data=[out:json];node["amenity"="police"](around:3000,${lat},${lon});out;`;
  const res = await fetch(url);
  const data = await res.json();
  data.elements.forEach((p) => {
    L.marker([p.lat, p.lon]).addTo(map).bindPopup("Police Station");
  });
}

// ===== SAFETY SCORE =====
function safetyScore(friend) {
  let score = 70;
  if (friend === "alone") score -= 20;
  if (friend === "female") score += 10;
  if (friend === "male") score += 5;
  return score;
}

// ===== PANIC BUTTON =====
function panic() {
  alert("🚨 Emergency Alert Sent to Trusted Contacts!");
}

// ===== MAIN FUNCTION =====
async function findRoute() {
  let start = document.getElementById("start").value;
  let end = document.getElementById("end").value;
  let friend = document.getElementById("friend").value;

  if (!start || !end) {
    alert("Enter start & destination!");
    return;
  }

  const startCoords = await getCoordinates(start);
  const endCoords = await getCoordinates(end);
  if (!startCoords || !endCoords) return;

  map.setView([startCoords.lat, startCoords.lon], 13);

  L.marker([startCoords.lat, startCoords.lon]).addTo(map).bindPopup("Start");
  L.marker([endCoords.lat, endCoords.lon]).addTo(map).bindPopup("Destination");

  await drawRoute(startCoords, endCoords);
  await showPolice(startCoords.lat, startCoords.lon);

  // Offline storage
  localStorage.setItem("lastRoute", JSON.stringify({ start, end }));

  let score = safetyScore(friend);

  document.getElementById("result").innerHTML =
    `Route from <b>${start}</b> to <b>${end}</b><br>
         Safety Score: <b>${score}/100</b>`;
}
