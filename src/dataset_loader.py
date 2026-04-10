import torch
from torch.utils.data import Dataset
import pandas as pd
import os
import random
import numpy as np

from mel_extractor import extract_mel
from audio_utils import load_waveform

label_map = {"bonafide": 0, "spoof": 1}


# ---------------- SpecAugment ----------------
def spec_augment(mel, freq_mask=10, time_mask=20):
    mel = mel.copy()

    # Frequency mask
    f = random.randint(0, freq_mask)
    if f > 0:
        f0 = random.randint(0, mel.shape[0] - f)
        mel[f0:f0+f, :] = 0

    # Time mask
    t = random.randint(0, time_mask)
    if t > 0:
        t0 = random.randint(0, mel.shape[1] - t)
        mel[:, t0:t0+t] = 0

    return mel


# ---------------- Wave Augmentation ----------------
def augment_waveform(wave):
    if random.random() < 0.3:
        gain = random.uniform(0.8, 1.2)
        wave = wave * gain

    if random.random() < 0.3:
        noise = torch.randn_like(wave) * 0.003
        wave = wave + noise

    if random.random() < 0.3:
        shift = random.randint(-800, 800)
        wave = torch.roll(wave, shifts=shift)

    return wave


# ---------------- Dataset ----------------
class ASVspoofDataset(Dataset):
    def __init__(self, protocol_path, base_audio_path, training=True):
        self.df = pd.read_csv(protocol_path, sep=" ", header=None)
        self.df.columns = ["speaker_id", "utt_id", "sysid", "attackid", "label"]
        self.base_audio_path = base_audio_path
        self.training = training

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        file_id = row["utt_id"]
        label = label_map[row["label"]]

        audio_path = os.path.join(self.base_audio_path, f"{file_id}.flac")

        mel = extract_mel(audio_path)
        wave = load_waveform(audio_path)

        if self.training:
            mel = spec_augment(mel)
            wave = augment_waveform(wave)

        mel = torch.from_numpy(np.array(mel)).float()
        wave = wave.clone().detach().float()

        return mel, wave, torch.tensor(label).long()
