import pandas as pd

path = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"

df = pd.read_csv(path, sep=" ", header=None)
print(df.head(10))
print("Total rows:", len(df))
