from mel_extractor import extract_mel
import matplotlib.pyplot as plt

audio_path = "../data/LA/ASVspoof2019_LA_train/flac/LA_T_1000137.flac"

mel = extract_mel(audio_path)
print("Mel shape:", mel.shape)

plt.imshow(mel, aspect='auto', origin='lower')
plt.title("Mel Spectrogram")
plt.colorbar()
plt.show()
