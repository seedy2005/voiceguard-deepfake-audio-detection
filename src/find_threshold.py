import torch
import numpy as np
from sklearn.metrics import roc_curve
from torch.utils.data import DataLoader
from model import CNNTransformer
from dataset_loader import ASVspoofDataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

EVAL_PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.eval.trl.txt"
EVAL_AUDIO   = "../data/LA/ASVspoof2019_LA_eval/flac"

T = torch.load("temperature.pt")

model = CNNTransformer().to(DEVICE)
ckpt = torch.load("../checkpoints/best_model.pth", map_location=DEVICE)
model.load_state_dict(ckpt["model_state"])
model.eval()

dataset = ASVspoofDataset(EVAL_PROTOCOL, EVAL_AUDIO)
loader = DataLoader(dataset, batch_size=8)

y_true = []
y_score = []

with torch.no_grad():
    for mel, wave, y in loader:
        mel = mel.unsqueeze(1).to(DEVICE)
        wave = wave.to(DEVICE)

        logits = model(mel, wave)
        probs = torch.softmax(logits / T, dim=1)[:,1]

        y_true.extend(y.numpy())
        y_score.extend(probs.cpu().numpy())

fpr, tpr, thresh = roc_curve(y_true, y_score)

eer = np.nanargmin(np.abs(fpr - (1 - tpr)))
print("Optimal Threshold:", thresh[eer])
