import os
import pandas as pd

protocol_path = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"

print("Checking file exists:", os.path.exists(protocol_path))

df = pd.read_csv(protocol_path, sep=" ", header=None)

df.columns = ["utt_id", "speaker", "system_id", "attack_id", "label"]

print(df.head())
print("Total samples:", len(df))
print(df["label"].value_counts())
