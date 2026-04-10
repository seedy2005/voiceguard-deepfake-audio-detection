from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import os
import numpy as np
import sys

# Allow importing from src/
sys.path.append("src")

from model import CNNTransformer
from mel_extractor import extract_mel
from audio_utils import load_waveform

# ================= CONFIG =================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CHECKPOINT_PATH = "checkpoints/best_model.pth"

ALLOW_TH = 0.50
CHALLENGE_TH = 0.80

# ================= APP =================
app = Flask(__name__)
CORS(app)

print("Using device:", DEVICE)

# ================= LOAD MODEL =================
model = CNNTransformer().to(DEVICE)
checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
model.load_state_dict(checkpoint["model_state"])
model.eval()

print("✅ Model loaded successfully")

# ================= DECISION ENGINE =================
def risk_decision(prob):
    if prob < ALLOW_TH:
        return "ALLOW"
    elif prob < CHALLENGE_TH:
        return "CHALLENGE"
    else:
        return "BLOCK"

# ================= ROOT =================
@app.route("/")
def home():
    return "Deepfake Audio Detection API Running"

# ================= PREDICT =================
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    temp_path = "temp_" + file.filename
    file.save(temp_path)

    try:
        mel = extract_mel(temp_path)
        wave = load_waveform(temp_path)

        if isinstance(mel, np.ndarray):
            mel = torch.from_numpy(mel)
        if isinstance(wave, np.ndarray):
            wave = torch.from_numpy(wave)

        mel = mel.float().unsqueeze(0).unsqueeze(0).to(DEVICE)
        wave = wave.float().unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            logits = model(mel, wave)
            probs = torch.softmax(logits, dim=1)

        spoof_prob = probs[:, 1].item()
        decision = risk_decision(spoof_prob)

        return jsonify({
            "prediction": "FAKE" if spoof_prob >= ALLOW_TH else "REAL",
            "confidence": round(spoof_prob, 4),
            "decision": decision
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)