const BASE_URL = "https://logsphere-backend.onrender.com";

async function loadDashboard() {
  try {
    const res = await fetch(BASE_URL + "/stats");
    const data = await res.json();

    document.getElementById("totalLogs").innerText = data.total;
    document.getElementById("errorLogs").innerText = data.error;
    document.getElementById("warningLogs").innerText = data.warning;
    document.getElementById("infoLogs").innerText = data.info;

    // Load logs
    const logRes = await fetch(BASE_URL + "/logs");
    const logs = await logRes.json();

    const table = document.getElementById("logTableBody");
    table.innerHTML = "";

    logs.forEach(log => {
      const row = `<tr>
        <td>${log.type}</td>
        <td>${log.message}</td>
      </tr>`;
      table.innerHTML += row;
    });

  } catch (err) {
    console.error("Error loading dashboard:", err);
  }
}
async function uploadLogFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(BASE_URL + "/upload-log", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    alert(data.message);

  } catch (err) {
    console.error("Upload error:", err);
  }
}