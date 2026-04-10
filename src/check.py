from collections import Counter
from dataset_loader import ASVspoofDataset

TRAIN_PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
TRAIN_AUDIO   = "../data/LA/ASVspoof2019_LA_train/flac"

train_dataset = ASVspoofDataset(TRAIN_PROTOCOL, TRAIN_AUDIO)

labels = [lab.item() for _, lab in train_dataset]

print("Label distribution:", Counter(labels))
