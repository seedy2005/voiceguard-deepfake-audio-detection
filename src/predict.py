import torch
import sys
import numpy as np

from model import CNNTransformer
from mel_extractor import extract_mel
from audio_utils import load_waveform


# ================= CONFIG =================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CHECKPOINT_PATH = "../checkpoints/best_model.pth"

# 🔐 SECURITY-ORIENTED THRESHOLDS
ALLOW_TH = 0.70        # Hard to allow
CHALLENGE_TH = 0.85    # Medium risk boundary

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
        return "ALLOW - Low Risk"

    elif prob < CHALLENGE_TH:
        return "CHALLENGE - Medium Risk"

    else:
        return "BLOCK - High Risk (Spoof Suspected)"


# ================= PREDICTION =================
def predict(audio_path):

    # ----- Feature Extraction -----
    mel = extract_mel(audio_path)
    wave = load_waveform(audio_path)

    # Safe tensor conversion
    if isinstance(mel, np.ndarray):
        mel = torch.from_numpy(mel)

    if isinstance(wave, np.ndarray):
        wave = torch.from_numpy(wave)

    mel = mel.float().unsqueeze(0).unsqueeze(0).to(DEVICE)
    wave = wave.float().unsqueeze(0).to(DEVICE)

    # ----- Model Forward -----
    with torch.no_grad():
        logits = model(mel, wave)

        # 🔥 Temperature scaling for stable confidence
        T = 1.8
        probs = torch.softmax(logits / T, dim=1)

    spoof_prob = probs[:, 1].item()
    decision = risk_decision(spoof_prob)

    print("\n========== SECURITY PREDICTION ==========")
    print(f"Audio File        : {audio_path}")
    print(f"Spoof Probability : {spoof_prob:.4f}")
    print(f"Decision          : {decision}")
    print("=========================================")

    return {
        "prediction": "FAKE" if spoof_prob >= ALLOW_TH else "REAL",
        "confidence": round(spoof_prob, 4),
        "decision": decision
    }


# ================= MAIN =================
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python predict.py <audio.wav>")
        sys.exit()

    audio_path = sys.argv[1]
    predict(audio_path)