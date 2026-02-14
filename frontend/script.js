async function predictDisease() {
    const symptoms = document.getElementById("symptoms").value.trim();

    if (!symptoms) {
        alert("Please enter symptoms");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/predict/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symptoms })
        });

        const data = await response.json();

        // Show prediction
        document.getElementById("diseaseName").innerText = data.disease;
        document.getElementById("probability").innerText = data.probability;

        document.getElementById("resultCard").classList.remove("hidden");
        document.getElementById("drugCard").classList.remove("hidden");

        // Show medicines
        const drugList = document.getElementById("drugList");
        drugList.innerHTML = "";

    data.medicines.forEach(med => {
    const li = document.createElement("li");

    li.innerHTML = `
        <b>${med.name}</b><br>
        <a href="${med.amazon}" target="_blank">Amazon</a> |
        <a href="${med.flipkart}" target="_blank">Flipkart</a> |
        <a href="${med.blinkit}" target="_blank">Blinkit</a> |
        <a href="${med.bigbasket}" target="_blank">BigBasket</a> |
        <a href="${med.apollo}" target="_blank">Apollo</a> |
        <a href="${med.tata1mg}" target="_blank">Tata 1mg</a> |
        <a href="${med.netmeds}" target="_blank">Netmeds</a>
        <hr>
    `;

    drugList.appendChild(li);
});



        // Save history
        saveHistory(symptoms, data.disease, data.probability);

    } catch (error) {
        console.error(error);
        alert("Backend not responding");
    }
}

function saveHistory(symptoms, disease, probability) {
    let history = JSON.parse(localStorage.getItem("medicalHistory")) || [];

    history.push({
        date: new Date().toLocaleString(),
        symptoms,
        disease,
        probability
    });

    localStorage.setItem("medicalHistory", JSON.stringify(history));
}

function loadHistory() {
    const historyList = document.getElementById("historyList");
    historyList.innerHTML = "";

    const history = JSON.parse(localStorage.getItem("medicalHistory")) || [];

    history.forEach(record => {
        const li = document.createElement("li");
        li.innerText = `${record.date} → ${record.disease} (${record.probability}%)`;
        historyList.appendChild(li);
    });
}

function downloadPDF() {
    // Backend-generated PDF
    window.open("http://127.0.0.1:8000/api/report/", "_blank");
}
