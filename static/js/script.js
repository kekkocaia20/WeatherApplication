const input = document.getElementById("cityInput");
const list = document.getElementById("autocomplete-list");

input.addEventListener("input", function() {
    const val = this.value;
    list.innerHTML = "";
    
    if (!val || val.length < 3) return;

    // Usiamo l'API di Nominatim (OpenStreetMap) per cercare le città
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${val}&addressdetails=1&limit=5`)
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                let div = document.createElement("DIV");
                // Mostra Città, Regione/Stato
                div.innerHTML = `<strong>${item.display_name}</strong>`;
                div.addEventListener("click", function() {
                    // Quando clicchi, prendi solo il nome della città (prima parte)
                    input.value = item.display_name.split(',')[0];
                    list.innerHTML = "";
                });
                list.appendChild(div);
            });
        });
});

// Chiudi la lista se l'utente clicca fuori
document.addEventListener("click", function (e) {
    if (e.target !== input) {
        list.innerHTML = "";
    }
});