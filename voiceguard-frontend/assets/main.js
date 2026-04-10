/**
 * VoiceGuard · Main Entry Point
 * Wires up all events: file upload, drag-drop, analyze, reset, export.
 */

// ─── DOM refs ───────────────────────────────────────────────────────────────
const dropZone      = document.getElementById("dropZone");
const fileInput     = document.getElementById("fileInput");
const browseBtn     = document.getElementById("browseBtn");
const fileSelected  = document.getElementById("fileSelected");
const fileNameEl    = document.getElementById("fileName");
const fileSizeEl    = document.getElementById("fileSize");
const removeFileBtn = document.getElementById("removeFile");
const analyzeBtn    = document.getElementById("analyzeBtn");
const uploadSection = document.getElementById("uploadSection");
const loadingPanel  = document.getElementById("loadingPanel");
const resultsPanel  = document.getElementById("resultsPanel");
const resetBtn      = document.getElementById("resetBtn");
const exportBtn     = document.getElementById("exportBtn");

// ─── State ──────────────────────────────────────────────────────────────────
let selectedFile = null;
let startTime    = null;

// ─── File Handling ───────────────────────────────────────────────────────────
function setFile(file) {
  if (!file || !file.type.startsWith("audio/")) {
    showToast("Please upload an audio file (MP3, WAV, M4A, OGG, FLAC…)");
    return;
  }
  selectedFile = file;
  fileNameEl.textContent = file.name;
  fileSizeEl.textContent = formatSize(file.size);
  fileSelected.classList.add("visible");
  analyzeBtn.disabled = false;
}

function clearFile() {
  selectedFile = null;
  fileInput.value = "";
  fileSelected.classList.remove("visible");
  analyzeBtn.disabled = true;
}

browseBtn.addEventListener("click",  ()  => fileInput.click());
dropZone.addEventListener("click",   (e) => { if (e.target !== browseBtn) fileInput.click(); });
fileInput.addEventListener("change", (e) => { if (e.target.files[0]) setFile(e.target.files[0]); });
removeFileBtn.addEventListener("click", (e) => { e.stopPropagation(); clearFile(); });

dropZone.addEventListener("dragover",  (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
dropZone.addEventListener("dragleave", ()  => dropZone.classList.remove("drag-over"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
});

// ─── Analyze Flow ────────────────────────────────────────────────────────────
analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  startTime = Date.now();

  // Switch to loading view
  uploadSection.style.display = "none";
  loadingPanel.classList.add("visible");
  resultsPanel.classList.remove("visible");
  resetSteps();
  animateSteps();

  try {
    const result = await callPredictAPI(selectedFile, startTime);

    await sleep(200); // small pause for polish
    loadingPanel.classList.remove("visible");
    displayResults(result);
    resultsPanel.classList.add("visible");

  } catch (err) {
    loadingPanel.classList.remove("visible");
    uploadSection.style.display = "";
    showToast("Analysis failed: " + err.message);
  }
});

// ─── Reset ───────────────────────────────────────────────────────────────────
resetBtn.addEventListener("click", () => {
  resultsPanel.classList.remove("visible");
  loadingPanel.classList.remove("visible");
  uploadSection.style.display = "";
  clearFile();
  resetGauge();
});

// ─── Export JSON Report ───────────────────────────────────────────────────────
exportBtn.addEventListener("click", () => {
  const report = {
    file:       selectedFile?.name,
    verdict:    document.getElementById("verdictWord").textContent,
    confidence: document.getElementById("gaugePct").textContent,
    risk:       document.getElementById("riskTitle").textContent,
    model:      document.getElementById("metricModel").textContent,
    latency:    document.getElementById("metricLatency").textContent,
    timestamp:  new Date().toISOString(),
  };
  const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "voiceguard-report-" + Date.now() + ".json";
  a.click();
  showToast("Report exported ✓");
});

// ─── Utility ─────────────────────────────────────────────────────────────────
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
