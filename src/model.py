import torch
import torch.nn as nn


class CNNTransformer(nn.Module):
    def __init__(self):
        super().__init__()

        # ---------------- MEL CNN BRANCH ----------------
        self.mel_cnn = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.AdaptiveAvgPool2d((1, 32))  # Output shape -> (B, 32, 1, 32)
        )

        # ---------------- WAVEFORM BRANCH ----------------
        self.wave_proj = nn.Linear(16000, 64)  # compress waveform

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=64,
            nhead=4,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=1
        )

        # ---------------- CLASSIFIER ----------------
        self.classifier = nn.Sequential(
            nn.Linear(96, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 2)
        )

    def forward(self, mel, wave):
        # ---------------- MEL BRANCH ----------------
        mel_feat = self.mel_cnn(mel)          # (B, 32, 1, 32)
        mel_feat = mel_feat.view(mel_feat.size(0), 32, 32)

        # Global pooling (IMPORTANT stabilization step)
        mel_feat = mel_feat.mean(dim=1)       # (B, 32)

        # ---------------- WAVEFORM BRANCH ----------------
        wave_feat = self.wave_proj(wave)      # (B, 64)

        # Transformer expects (B, seq, dim)
        wave_feat = wave_feat.unsqueeze(1)    # (B, 1, 64)

        wave_feat = self.transformer(wave_feat)

        wave_feat = wave_feat.squeeze(1)      # (B, 64)

        # ---------------- FUSION ----------------
        combined = torch.cat([mel_feat, wave_feat], dim=1)  # (B, 96)

        # ---------------- CLASSIFIER ----------------
        output = self.classifier(combined)

        return output
