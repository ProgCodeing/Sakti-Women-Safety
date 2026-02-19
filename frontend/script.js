async function findRoute() {
  let start = document.getElementById("start").value;
  let end = document.getElementById("end").value;
  let friend = document.getElementById("friend").value;

  let res = await fetch(
    "https://sakti-women-safety-production.up.railway.app/route",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, end, friend }),
    },
  );

  let data = await res.json();
  document.getElementById("result").innerHTML =
    "Recommended Route: " + data.route;

  var map = L.map("map").setView([20.0, 73.78], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "Map data © OpenStreetMap",
  }).addTo(map);
}
