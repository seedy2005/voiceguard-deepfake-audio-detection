import torch
from model import CNNBiLSTM

model = CNNBiLSTM()

dummy_input = torch.randn(1, 1, 128, 300)  # (batch, channel, freq, time)

output = model(dummy_input)

print("Output shape:", output.shape)
print("Output:", output)
