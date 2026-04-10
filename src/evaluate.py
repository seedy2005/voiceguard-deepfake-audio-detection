import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

from model import CNNTransformer
from dataset_loader import ASVspoofDataset


# ================= CONFIG =================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BATCH_SIZE = 8

# Binary threshold for metrics (security-focused)
BINARY_THRESHOLD = 0.50

# Tri-state policy thresholds (demo layer)
ALLOW_THRESHOLD = 0.55
CHALLENGE_THRESHOLD = 0.85

EVAL_PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.eval.trl.txt"
EVAL_AUDIO   = "../data/LA/ASVspoof2019_LA_eval/flac"

CHECKPOINT_PATH = "../checkpoints/best_model.pth"


def main():

    print("Using device:", DEVICE)

    # ---------- Load Model ----------
    model = CNNTransformer().to(DEVICE)
    checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    print("Model loaded successfully")

    # ---------- Dataset ----------
    eval_dataset = ASVspoofDataset(EVAL_PROTOCOL, EVAL_AUDIO)

    eval_loader = DataLoader(
        eval_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )

    # ---------- Evaluation ----------
    all_preds = []
    all_labels = []

    allowed = 0
    challenged = 0
    blocked = 0

    with torch.no_grad():
        for mel, wave, labels in eval_loader:

            mel = mel.unsqueeze(1).to(DEVICE)
            wave = wave.to(DEVICE)
            labels = labels.to(DEVICE)

            logits = model(mel, wave)
            probs = torch.softmax(logits, dim=1)[:, 1]

            for prob, label in zip(probs, labels):

                prob = prob.item()

                # ===== Binary Decision (for metrics) =====
                binary_decision = 1 if prob >= BINARY_THRESHOLD else 0
                all_preds.append(binary_decision)
                all_labels.append(label.item())

                # ===== Tri-State Policy (for demo) =====
                if prob < ALLOW_THRESHOLD:
                    allowed += 1
                elif prob < CHALLENGE_THRESHOLD:
                    challenged += 1
                else:
                    blocked += 1

    # ---------- Metrics ----------
    acc = accuracy_score(all_labels, all_preds)
    prec = precision_score(all_labels, all_preds)
    rec = recall_score(all_labels, all_preds)
    cm = confusion_matrix(all_labels, all_preds)

    print("\n========== FINAL RESULTS ==========")
    print(f"Allowed   : {allowed}")
    print(f"Challenged: {challenged}")
    print(f"Blocked   : {blocked}")

    print(f"\nBinary Threshold Used: {BINARY_THRESHOLD}")
    print(f"Accuracy  : {acc*100:.2f}%")
    print(f"Precision : {prec*100:.2f}%")
    print(f"Recall    : {rec*100:.2f}%")

    print("\nConfusion Matrix:")
    print(cm)


if __name__ == "__main__":
    main()