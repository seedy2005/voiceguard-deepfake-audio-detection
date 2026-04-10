from dataset_loader import ASVspoofDataset

dataset = ASVspoofDataset(
    protocol_path="../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt",
    base_audio_path="../data/LA/ASVspoof2019_LA_train/flac"
)

mel, label = dataset[0]
print(mel.shape, label)
