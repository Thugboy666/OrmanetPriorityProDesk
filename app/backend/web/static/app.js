const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".tab-panel");

const resultsList = document.getElementById("clienti-results");
const searchInput = document.getElementById("search-clienti");
const detailContainer = document.getElementById("cliente-dettaglio");

function activateTab(name) {
  tabs.forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.tab === name);
  });
  panels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === `tab-${name}`);
  });
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => activateTab(tab.dataset.tab));
});

document.querySelectorAll("button[data-import]").forEach((button) => {
  button.addEventListener("click", async () => {
    const target = button.dataset.import;
    const input = document.getElementById(`upload-${target}`);
    const status = document.querySelector(`[data-status='${target}']`);

    if (!input.files.length) {
      status.textContent = "Seleziona un file .xlsx";
      return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    status.textContent = "Importazione in corso...";
    try {
      const response = await fetch(`/api/import/${target}`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Errore importazione");
      }
      status.textContent = `Import completato (${data.rows} righe)`;
    } catch (error) {
      status.textContent = error.message;
    }
  });
});

let searchTimeout = null;
searchInput.addEventListener("input", () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(async () => {
    const query = searchInput.value.trim();
    const response = await fetch(`/api/clienti?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    resultsList.innerHTML = "";
    data.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item.ragione_sociale;
      li.addEventListener("click", () => loadCliente(item.ragione_sociale));
      resultsList.appendChild(li);
    });
  }, 300);
});

async function loadCliente(ragioneSociale) {
  activateTab("dettaglio");
  detailContainer.innerHTML = "Caricamento...";
  try {
    const response = await fetch(`/api/cliente/${encodeURIComponent(ragioneSociale)}`);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Errore caricamento");
    }
    detailContainer.innerHTML = `
      <div><strong>Ragione sociale:</strong> ${data.ragione_sociale}</div>
      <div><strong>Listino:</strong> ${data.listino ?? "-"}</div>
      <div><strong>Porto franco:</strong> ${data.porto_franco}</div>
      <div><strong>Minimo ordine:</strong> ${data.min_ord ?? "-"}</div>
      <div><strong>Porto assegnato:</strong> ${data.porto_assegnato ? "Sì" : "No"}</div>
      <div><strong>Drop:</strong> ${data.drop ? "Sì" : "No"}</div>
    `;
  } catch (error) {
    detailContainer.textContent = error.message;
  }
}
