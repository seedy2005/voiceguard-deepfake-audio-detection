import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from model import CNNTransformer
from dataset_loader import ASVspoofDataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DEV_PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.dev.trl.txt"
DEV_AUDIO   = "../data/LA/ASVspoof2019_LA_dev/flac"

model = CNNTransformer().to(DEVICE)
ckpt = torch.load("../checkpoints/best_model.pth", map_location=DEVICE)
model.load_state_dict(ckpt["model_state"])
model.eval()

dataset = ASVspoofDataset(DEV_PROTOCOL, DEV_AUDIO)
loader = DataLoader(dataset, batch_size=8)

logits = []
labels = []

with torch.no_grad():
    for mel, wave, y in loader:
        mel = mel.unsqueeze(1).to(DEVICE)
        wave = wave.to(DEVICE)

        out = model(mel, wave)
        logits.append(out.cpu())
        labels.append(y)

logits = torch.cat(logits)
labels = torch.cat(labels)

T = torch.ones(1, requires_grad=True)

optimizer = torch.optim.LBFGS([T], lr=0.01)

def loss_fn():
    probs = F.log_softmax(logits / T, dim=1)
    return F.nll_loss(probs, labels)

for _ in range(50):
    optimizer.zero_grad()
    loss = loss_fn()
    loss.backward()
    optimizer.step(loss_fn)

print("Optimal Temperature:", T.item())
torch.save(T.item(), "temperature.pt")
