const API_BASE = "https://disease-prediction-and-drug-79y4.onrender.com/api";

function addSymptom(symptom) {
    const input = document.getElementById("symptoms");
    const current = input.value.split(",").map(item => item.trim()).filter(Boolean);
    if (!current.some(item => item.toLowerCase() === symptom)) current.push(symptom);
    input.value = current.join(", ");
    input.focus();
}

async function predictDisease() {
    const symptoms = document.getElementById("symptoms").value.trim();
    const button = document.getElementById("predictButton");

    if (!symptoms) {
        document.getElementById("symptoms").focus();
        return;
    }

    button.disabled = true;
    button.querySelector("span").textContent = "Reading symptoms...";

    try {
        const response = await fetch(`${API_BASE}/predict/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symptoms })
        });

        const data = await response.json();
        if (!response.ok || data.error) throw new Error(data.error || "Prediction failed");

        document.getElementById("diseaseName").textContent = data.disease;
        document.getElementById("probability").textContent = data.probability;
        document.getElementById("confidenceBar").style.width = `${Math.min(Number(data.probability), 100)}%`;

        document.getElementById("resultCard").classList.remove("hidden");
        document.getElementById("drugCard").classList.remove("hidden");

        const drugList = document.getElementById("drugList");
        drugList.innerHTML = (data.medicines || []).map((med, index) => `
            <article class="medicine-card">
                <span class="medicine-number">OPTION ${String(index + 1).padStart(2, "0")}</span>
                <h3>${escapeHtml(med.name)}</h3>
                <div class="store-links">${storeLinks(med)}</div>
            </article>
        `).join("");
        saveHistory(symptoms, data.disease, data.probability);
        loadHistory();
        document.getElementById("drugCard").scrollIntoView({ behavior: "smooth", block: "start" });

    } catch (error) {
        console.error(error);
        alert(`We couldn't complete the check: ${error.message}`);
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent = "Analyze symptoms";
    }
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value || "Care option";
    return div.innerHTML;
}

function storeLinks(medicine) {
    const stores = [["Amazon", medicine.amazon], ["Flipkart", medicine.flipkart], ["Blinkit", medicine.blinkit], ["BigBasket", medicine.bigbasket], ["Apollo", medicine.apollo], ["Tata 1mg", medicine.tata1mg], ["Netmeds", medicine.netmeds]];
    return stores.filter(([, url]) => url).map(([name, url]) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${name}</a>`).join("");
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

    if (!history.length) {
        historyList.innerHTML = '<p class="empty-state">Your recent checks will appear here.</p>';
        return;
    }
    history.slice(-4).reverse().forEach(record => {
        const item = document.createElement("div");
        item.className = "history-item";
        item.innerHTML = `<div><strong>${escapeHtml(record.disease)}</strong><small>${escapeHtml(record.date)} · ${escapeHtml(record.symptoms)}</small></div><span class="history-score">${escapeHtml(record.probability)}%</span>`;
        historyList.appendChild(item);
    });
}

function downloadPDF() {
    // Backend-generated PDF
    window.open(`${API_BASE}/report/`, "_blank");
}

loadHistory();
