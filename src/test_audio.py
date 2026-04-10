import librosa
import matplotlib.pyplot as plt

audio_path = "../data/LA/ASVspoof2019_LA_train/flac/LA_T_1000137.flac"



audio, sr = librosa.load(audio_path, sr=16000)
print("Audio Length:", len(audio))
print("Sample Rate:", sr)

plt.figure(figsize=(10,4))
plt.plot(audio)
plt.title("Waveform")
plt.show()
