import librosa
import numpy as np

def extract_mel(filepath, sr=16000, n_mels=128, max_len=300):
    audio, _ = librosa.load(filepath, sr=16000, duration=1.0)


    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_mels=n_mels
    )
    mel = librosa.power_to_db(mel, ref=np.max)

    # Normalize
    mel = (mel - mel.mean()) / (mel.std() + 1e-6)

    # Pad or truncate to fixed length
    if mel.shape[1] < max_len:
        pad_width = max_len - mel.shape[1]
        mel = np.pad(mel, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mel = mel[:, :max_len]

    return mel
