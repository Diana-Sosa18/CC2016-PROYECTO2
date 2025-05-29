let selectedStyle = "";
let selectedOcasion = "";
let detectedClima = "";

// Estilo → Ocasion
document.querySelectorAll(".style-option").forEach(option => {
    option.addEventListener("click", () => {
        selectedStyle = option.textContent;
        document.getElementById("stylesScreen").classList.add("hidden");
        document.getElementById("ocasionScreen").classList.remove("hidden");
    });
});

// Ocasion → Clima
document.querySelectorAll(".ocasion-option").forEach(option => {
    option.addEventListener("click", () => {
        selectedOcasion = option.dataset.ocasion;
        document.getElementById("ocasionScreen").classList.add("hidden");
        document.getElementById("climaScreen").classList.remove("hidden");

        // Clima detectado automáticamente
        fetch("/api/weather")
            .then(res => res.json())
            .then(data => {
                detectedClima = data.clima;
                document.getElementById("weatherResult").innerText = `Clima: ${detectedClima}`;
            });
    });
});

// Clima → Recomendaciones
document.getElementById("continuarBtn").addEventListener("click", () => {
    const payload = {
        estilo: selectedStyle,
        clima: detectedClima,
        ocasion: selectedOcasion
    };

    fetch("/recommend", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        console.log("🎯 Recomendaciones:", data);
    });
});


function mostrarRecomendaciones(outfits) {
    const outfitsGrid = document.querySelector(".outfits-grid");
    outfitsGrid.innerHTML = ""; // Limpiar recomendaciones anteriores

    outfits.forEach((outfit, index) => {
        const card = document.createElement("div");
        card.className = "outfit-card";
        card.dataset.outfit = index;

        const img = document.createElement("img");
        img.src = `/static/images/outfits/${outfit.ID_Image}.png`;
        img.alt = `Outfit ${index + 1}`;
        img.className = "outfit-image";

        card.appendChild(img);
        outfitsGrid.appendChild(card);
    });

    // Mostrar la pantalla de outfits
    document.getElementById("climaScreen").classList.add("hidden");
    document.getElementById("outfitsScreen").classList.remove("hidden");

    // Mostrar botones de acción
    document.getElementById("outfitActions").classList.remove("hidden");
}

// Al recibir la respuesta de /recommend
document.getElementById("continuarBtn").addEventListener("click", () => {
    const payload = {
        estilo: selectedStyle,
        clima: detectedClima,
        ocasion: selectedOcasion
    };

    fetch("/recommend", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        console.log("🎯 Recomendaciones recibidas:", data);
        mostrarRecomendaciones(data);
    });
});
