# VoiceGuard · Backend Connection Guide

## File Structure

```
voiceguard-frontend/
├── index.html              ← Entry point
├── CONNECT_GUIDE.md        ← This file
├── api/
│   ├── config.js           ← ⭐ Edit this to point to your backend
│   └── predict.js          ← Handles the POST /predict request
├── assets/
│   ├── style.css           ← All styles
│   └── main.js             ← App logic & event wiring
└── components/
    ├── ui.js               ← Toast, steps, results rendering
    └── gauge.js            ← Animated gauge meter
```

---

## Step 1 — Set Your Backend URL

Open **`api/config.js`** and change `BASE_URL`:

```js
const API_CONFIG = {
  BASE_URL: "http://127.0.0.1:5000",   // ← your Flask port
  PREDICT_ENDPOINT: "/predict",
  TIMEOUT_MS: 30000,
  DEMO_FALLBACK: true,                  // set false when API is live
};
```

| Backend | Default URL |
|---------|-------------|
| Flask   | `http://127.0.0.1:5000` |
| FastAPI | `http://127.0.0.1:8000` |
| Deployed| `https://api.yourdomain.com` |

---

## Step 2 — Expected API Response

Your `/predict` endpoint must return JSON in this shape:

```json
{
  "label":      "REAL",
  "confidence": 0.94,
  "model":      "YourModelName",
  "latency":    "1.23s"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `label` | `"REAL"` or `"FAKE"` | ✅ | Case-insensitive |
| `confidence` | float `0.0–1.0` | ✅ | e.g. `0.87` = 87% |
| `model` | string | optional | Shown in the UI |
| `latency` | string | optional | Computed client-side if absent |

---

## Step 3 — Enable CORS in Your Flask App

The browser will block requests if your Flask app doesn't allow CORS.

### Install flask-cors
```bash
pip install flask-cors
```

### Add to app.py
```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # allows all origins (fine for development)

# For production, restrict to your frontend domain:
# CORS(app, origins=["https://yourfrontend.com"])

@app.route('/predict', methods=['POST'])
def predict():
    audio_file = request.files['file']     # matches FormData key in predict.js
    
    # --- Your model inference here ---
    # result = your_model.predict(audio_file)
    
    return jsonify({
        "label":      "REAL",              # or "FAKE"
        "confidence": 0.94,
        "model":      "YourModel v1.0",
        "latency":    "1.12s"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Step 4 — Run Everything

### Start your Flask backend
```bash
cd /path/to/your/project
source .venv/bin/activate
python app.py
```

### Open the frontend
Option A — open `index.html` directly in your browser (file://)
Option B — serve it with Python for proper CORS handling:

```bash
cd voiceguard-frontend
python -m http.server 3000
# then visit http://localhost:3000
```

---

## Step 5 — Turn Off Demo Mode

Once your backend is running correctly, open `api/config.js` and set:

```js
DEMO_FALLBACK: false,
```

This disables the simulated response and routes all requests to your real API.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| CORS error in browser console | Add `flask-cors` and `CORS(app)` — see Step 3 |
| `Failed to fetch` | Check `BASE_URL` in `config.js` matches Flask port |
| `405 Method Not Allowed` | Ensure `methods=['POST']` on your route |
| `400 Bad Request` | Check the file field name: must be `request.files['file']` |
| Results show "Demo Mode" | API unreachable; check Flask is running |
| File upload works but wrong result | Verify your model returns `label` + `confidence` |

---

## Production Checklist

- [ ] Set `BASE_URL` to your deployed backend URL
- [ ] Set `DEMO_FALLBACK: false`
- [ ] Restrict CORS to your frontend domain only
- [ ] Add HTTPS to your backend
- [ ] Add an auth token header if your API requires it (see `predict.js`)
