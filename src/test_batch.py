import torch
from model import CNNTransformer

device = torch.device("cuda")
model = CNNTransformer().to(device)

# Fake input shaped like your real model input
# Adjust mel and wave sizes to match your dataset
mel = torch.randn(1, 1, 80, 300).to(device)
wave = torch.randn(1, 16000).to(device)

batch = 1

while True:
    try:
        print(f"Trying batch size: {batch}")
        mel_b = mel.repeat(batch, 1, 1, 1)
        wave_b = wave.repeat(batch, 1)
        out = model(mel_b, wave_b)
        torch.cuda.synchronize()
        batch *= 2
    except RuntimeError as e:
        print("Max batch size exceeded at:", batch)
        break
