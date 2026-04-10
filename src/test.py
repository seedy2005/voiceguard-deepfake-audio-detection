from dataset_loader import ASVspoofDataset

PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
AUDIO = "../data/LA/ASVspoof2019_LA_train/flac"

dataset = ASVspoofDataset(PROTOCOL, AUDIO)

mel, wave, label = dataset[0]

print("Mel shape:", mel.shape)
print("Wave shape:", wave.shape)
print("Label:", label)
