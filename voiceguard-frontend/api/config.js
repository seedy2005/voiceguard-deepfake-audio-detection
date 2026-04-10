/**
 * ╔══════════════════════════════════════════════════════════════╗
 * ║              VoiceGuard · API Configuration                  ║
 * ║                                                              ║
 * ║  Edit API_BASE_URL to point to your Flask / FastAPI backend. ║
 * ╚══════════════════════════════════════════════════════════════╝
 *
 * LOCAL DEVELOPMENT
 *   Flask default  → http://127.0.0.1:5000
 *   FastAPI default→ http://127.0.0.1:8000
 *
 * PRODUCTION
 *   Change to your deployed server URL, e.g.:
 *   https://api.yourdomain.com
 */

const API_CONFIG = {
  // ← Change this to match your backend
  BASE_URL: "http://127.0.0.1:5000",

  // Endpoint path (matches @app.route('/predict') in Flask)
  PREDICT_ENDPOINT: "/predict",

  // Request timeout in milliseconds
  TIMEOUT_MS: 30000,

  // Set to false to disable the demo fallback
  // (demo fallback activates when the API is unreachable)
  DEMO_FALLBACK: true,
};
