import librosa
import torch
import numpy as np


def load_waveform(filepath, sr=16000, duration=1.0):
    """
    Loads only first 'duration' seconds
    Prevents huge memory allocation
    """

    # ✅ Load limited duration
    wave, _ = librosa.load(
        filepath,
        sr=sr,
        duration=duration,
        mono=False
    )

    # Stereo → Mono
    if wave.ndim > 1:
        wave = np.mean(wave, axis=0)

    target_len = int(sr * duration)

    # Pad / Trim
    if len(wave) < target_len:
        wave = np.pad(wave, (0, target_len - len(wave)))
    else:
        wave = wave[:target_len]

    return torch.tensor(wave).float()