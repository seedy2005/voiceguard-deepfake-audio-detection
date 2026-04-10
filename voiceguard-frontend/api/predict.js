/**
 * VoiceGuard · API Module
 * Sends audio file to the /predict endpoint and returns structured result.
 *
 * Your app.py returns:
 * {
 *   "prediction": "REAL" | "FAKE",    ← mapped → data.label
 *   "confidence": 0.0 – 1.0,          ← spoof_prob (raw float, e.g. 0.8734)
 *   "decision":   "ALLOW" | "CHALLENGE" | "BLOCK"  ← mapped → data.risk
 * }
 *
 * This module normalises those into the shape the UI components expect:
 * {
 *   label, confidence, risk, latency, model
 * }
 */

/**
 * Send audio file to /predict and return the normalised result.
 * @param {File}   file      - The audio File object from the input
 * @param {number} startTime - Date.now() captured at upload start
 * @returns {Promise<Object>} Normalised prediction result
 */
async function callPredictAPI(file, startTime) {
  const url = API_CONFIG.BASE_URL + API_CONFIG.PREDICT_ENDPOINT;

  const formData = new FormData();
  formData.append("file", file); // matches: request.files['file'] in app.py

  const controller = new AbortController();
  const timeoutId  = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT_MS);

  try {
    const response = await fetch(url, {
      method: "POST",
      body:   formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errMsg = `Server returned ${response.status}`;
      try {
        const errBody = await response.json();
        if (errBody.error || errBody.message) errMsg = errBody.error || errBody.message;
      } catch (_) {}
      throw new Error(errMsg);
    }

    const raw = await response.json();

    /*
     * ── Normalise your app.py response ──────────────────────────────────
     *
     *  app.py field   →   UI field
     *  ─────────────────────────────
     *  prediction     →   label       ("REAL" / "FAKE")
     *  confidence     →   confidence  (0.0–1.0 spoof probability)
     *  decision       →   risk        ("ALLOW" / "CHALLENGE" / "BLOCK")
     */
    return {
      label:      (raw.prediction || "REAL").toUpperCase(),
      confidence: raw.confidence ?? 0,
      risk:       (raw.decision   || "ALLOW").toUpperCase(),
      model:      "CNNTransformer",
      latency:    ((Date.now() - startTime) / 1000).toFixed(2) + "s",
    };

  } catch (err) {
    clearTimeout(timeoutId);

    // ── DEMO FALLBACK ────────────────────────────────────────────────────
    // Mirrors your app.py thresholds: ALLOW < 0.50, CHALLENGE < 0.80, BLOCK ≥ 0.80
    // Set DEMO_FALLBACK: false in config.js once your backend is live.
    if (API_CONFIG.DEMO_FALLBACK && isNetworkError(err)) {
      console.warn("[VoiceGuard] API unreachable — using demo fallback.");
      await sleep(3200);
      const spoofProb = parseFloat((Math.random()).toFixed(4));
      const isFake    = spoofProb >= 0.50;
      const risk      = spoofProb <= 0.30 ? "ALLOW" : spoofProb < 0.80 ? "CHALLENGE" : "BLOCK";
      return {
        label:      isFake ? "FAKE" : "REAL",
        confidence: spoofProb,
        risk,
        model:      "Demo Mode",
        latency:    ((Date.now() - startTime) / 1000).toFixed(2) + "s",
      };
    }
    // ────────────────────────────────────────────────────────────────────

    throw err;
  }
}

/** Returns true for fetch-level network failures (not HTTP errors) */
function isNetworkError(err) {
  return (
    err.name === "AbortError" ||
    err.message.includes("Failed to fetch") ||
    err.message.includes("NetworkError") ||
    err.message.includes("Load failed") ||
    err.message.includes("404")
  );
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
