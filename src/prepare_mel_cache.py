import os
import torch
import pandas as pd
from mel_extractor import extract_mel

PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
AUDIO_DIR = "../data/LA/ASVspoof2019_LA_train/flac"
SAVE_DIR = "../data/mel_cache_train"

os.makedirs(SAVE_DIR, exist_ok=True)

df = pd.read_csv(PROTOCOL, sep=" ", header=None)
df.columns = ["speaker_id", "utt_id", "sysid", "attackid", "label"]

for idx, row in df.iterrows():
    file_id = row["utt_id"]
    audio_path = os.path.join(AUDIO_DIR, f"{file_id}.flac")
    save_path = os.path.join(SAVE_DIR, f"{file_id}.pt")

    if os.path.exists(save_path):
        continue

    mel = extract_mel(audio_path)
    torch.save(torch.tensor(mel).float(), save_path)

    if idx % 500 == 0:
        print(f"Processed {idx}/{len(df)}")
