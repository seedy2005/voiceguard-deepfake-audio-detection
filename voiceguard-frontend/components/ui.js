/**
 * VoiceGuard · UI Helpers
 * Toast notifications, loading steps, results rendering.
 */

// ─── Toast ─────────────────────────────────────────────────────────────────
function showToast(msg) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3200);
}

// ─── Loading Steps ──────────────────────────────────────────────────────────
const STEP_IDS     = ["step1", "step2", "step3", "step4"];
const STEP_LABELS  = [
  "Extracting spectral features",
  "Running neural classifier",
  "Calibrating confidence score",
  "Computing risk assessment",
];

function resetSteps() {
  STEP_IDS.forEach((id) => {
    const el = document.getElementById(id);
    el.classList.remove("active", "done");
  });
}

function animateSteps() {
  let i = 0;
  function next() {
    if (i > 0) {
      document.getElementById(STEP_IDS[i - 1]).classList.remove("active");
      document.getElementById(STEP_IDS[i - 1]).classList.add("done");
    }
    if (i < STEP_IDS.length) {
      document.getElementById(STEP_IDS[i]).classList.add("active");
      document.getElementById("loadingLabel").textContent = STEP_LABELS[i] + "…";
      i++;
      setTimeout(next, 900);
    }
  }
  next();
}

// ─── Display Results ────────────────────────────────────────────────────────
function displayResults(data) {
  const isReal = data.label === "REAL";

  /*
   * spoof_prob: 0.0 = definitely real, 1.0 = definitely fake
   * Gauge shows the model certainty in its verdict.
   */
  const spoofPct = Math.round(data.confidence * 100);
  const authPct  = 100 - spoofPct;
  const fakePct  = spoofPct;
  const gaugeVal = isReal ? authPct : spoofPct;

  /*
   * Three verdict states:
   *   REAL  + spoof_prob <= 0.30  → green  "AUTHENTIC"
   *   REAL  + spoof_prob >  0.30  → yellow "CHALLENGE"
   *   FAKE                        → red    "DEEPFAKE"
   */
  const isChallenge = isReal && data.confidence > 0.30;

  const verdictCard = document.getElementById("verdictCard");
  const checkIcon   = document.getElementById("verdictCheck");
  const xIcon       = document.getElementById("verdictX");

  // Create warning SVG icon once
  let warnIcon = document.getElementById("verdictWarn");
  if (!warnIcon) {
    warnIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    warnIcon.id = "verdictWarn";
    warnIcon.setAttribute("viewBox", "0 0 24 24");
    warnIcon.innerHTML =
      '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>' +
      '<line x1="12" y1="9" x2="12" y2="13"/>' +
      '<line x1="12" y1="17" x2="12.01" y2="17"/>';
    document.getElementById("verdictIcon").appendChild(warnIcon);
  }

  if (isChallenge) {
    verdictCard.className = "result-verdict challenge-verdict";
    document.getElementById("verdictWord").textContent  = "CHALLENGE";
    document.getElementById("verdictLabel").textContent = "NEEDS REVIEW";
    document.getElementById("verdictSub").textContent   = "Suspicious patterns detected. Manual review recommended.";
    checkIcon.style.display = "none";
    xIcon.style.display     = "none";
    warnIcon.style.display  = "block";
  } else if (isReal) {
    verdictCard.className = "result-verdict real";
    document.getElementById("verdictWord").textContent  = "AUTHENTIC";
    document.getElementById("verdictLabel").textContent = "VERIFIED REAL";
    document.getElementById("verdictSub").textContent   = "This audio appears to be a genuine human voice.";
    checkIcon.style.display = "block";
    xIcon.style.display     = "none";
    warnIcon.style.display  = "none";
  } else {
    verdictCard.className = "result-verdict fake";
    document.getElementById("verdictWord").textContent  = "DEEPFAKE";
    document.getElementById("verdictLabel").textContent = "DETECTED FAKE";
    document.getElementById("verdictSub").textContent   = "Synthetic or manipulated audio detected.";
    checkIcon.style.display = "none";
    xIcon.style.display     = "block";
    warnIcon.style.display  = "none";
  }

  // Gauge — amber color for challenge state
  animateGauge(gaugeVal, isChallenge ? "challenge" : isReal);

  // Metrics
  document.getElementById("metricAuth").textContent    = authPct + "%";
  document.getElementById("metricFake").textContent    = fakePct + "%";
  document.getElementById("metricModel").textContent   = data.model   || "VoiceGuard v3";
  document.getElementById("metricLatency").textContent = data.latency || "—";

  setTimeout(() => {
    document.getElementById("barAuth").style.width = authPct + "%";
    document.getElementById("barFake").style.width = fakePct + "%";
  }, 300);

  /*
   * Risk level — frontend overrides: spoof_prob > 0.30 → at least CHALLENGE
   * Backend BLOCK still applies if stricter.
   */
  const RISK_RANK    = { ALLOW: 0, CHALLENGE: 1, BLOCK: 2 };
  const backendRisk  = (data.risk || "ALLOW").toUpperCase();
  const frontendRisk = data.confidence > 0.30 ? "CHALLENGE" : "ALLOW";
  const riskRaw      = RISK_RANK[backendRisk] >= RISK_RANK[frontendRisk] ? backendRisk : frontendRisk;

  const RISK_MAP = {
    ALLOW: {
      cls:   "allow",
      title: "Allow",
      desc:  "Audio passes authenticity checks. Safe to proceed.",
      icon:  '<polyline points="20 6 9 17 4 12"/>',
    },
    CHALLENGE: {
      cls:   "challenge",
      title: "Challenge",
      desc:  "Uncertain authenticity. Further verification recommended.",
      icon:  '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
    },
    BLOCK: {
      cls:   "block",
      title: "Block",
      desc:  "High-confidence deepfake detected. Access denied.",
      icon:  '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    },
  };

  const riskInfo = RISK_MAP[riskRaw] || RISK_MAP.ALLOW;
  document.getElementById("riskCard").className    = "risk-card " + riskInfo.cls;
  document.getElementById("riskLevel").textContent = "RISK LEVEL — " + riskRaw;
  document.getElementById("riskTitle").textContent = riskInfo.title;
  document.getElementById("riskDesc").textContent  = riskInfo.desc;
  document.getElementById("riskIcon").innerHTML    = riskInfo.icon;
}

// ─── Format file size ───────────────────────────────────────────────────────
function formatSize(bytes) {
  if (bytes < 1024)           return bytes + " B";
  if (bytes < 1024 * 1024)   return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
}
