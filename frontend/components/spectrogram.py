import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import tempfile
import os


# ================================
# FORENSIC SPECTROGRAM SETTINGS
# ================================

DPI = 300
FIG_SIZE_STREAMLIT = (10, 4)
FIG_SIZE_PDF = (8, 3)


# ================================
# DISPLAY FORENSIC SPECTROGRAM
# ================================

def render_spectrogram(uploaded_file):

    try:

        suffix = uploaded_file.name.split(".")[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:

            tmp.write(uploaded_file.getvalue())

            audio_path = tmp.name


        y, sr = librosa.load(audio_path, sr=None)

        if len(y) == 0:

            st.warning("Empty audio file.")

            return


        # High resolution mel spectrogram
        S = librosa.feature.melspectrogram(

            y=y,
            sr=sr,
            n_fft=2048,
            hop_length=512,
            n_mels=128,
            fmax=8000   # forensic focus range
        )

        S_dB = librosa.power_to_db(S, ref=np.max)


        fig, ax = plt.subplots(
            figsize=FIG_SIZE_STREAMLIT,
            dpi=DPI
        )

        img = librosa.display.specshow(

            S_dB,
            sr=sr,
            hop_length=512,
            x_axis="time",
            y_axis="mel",
            cmap="inferno",
            fmax=8000,
            ax=ax

        )

        ax.set_title("Forensic Mel Spectrogram", fontsize=12)

        ax.set_xlabel("Time (seconds)")

        ax.set_ylabel("Frequency (Hz)")


        cbar = fig.colorbar(img, ax=ax)

        cbar.set_label("Intensity (dB)")


        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    except Exception as e:

        st.warning(f"Spectrogram error: {e}")


# ================================
# GENERATE HIGH-RES FILE FOR PDF
# ================================

def generate_spectrogram_file(uploaded_file):

    try:

        suffix = uploaded_file.name.split(".")[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:

            tmp.write(uploaded_file.getvalue())

            audio_path = tmp.name


        y, sr = librosa.load(audio_path, sr=None)

        if len(y) == 0:

            return None


        S = librosa.feature.melspectrogram(

            y=y,
            sr=sr,
            n_fft=2048,
            hop_length=512,
            n_mels=128,
            fmax=8000

        )

        S_dB = librosa.power_to_db(S, ref=np.max)


        spectrogram_path = os.path.join(

            tempfile.gettempdir(),
            "forensic_spectrogram.png"

        )


        fig, ax = plt.subplots(

            figsize=FIG_SIZE_PDF,
            dpi=DPI

        )

        img = librosa.display.specshow(

            S_dB,
            sr=sr,
            hop_length=512,
            x_axis="time",
            y_axis="mel",
            cmap="inferno",
            fmax=8000,
            ax=ax

        )

        ax.set_title("Forensic Mel Spectrogram")

        ax.set_xlabel("Time (seconds)")

        ax.set_ylabel("Frequency (Hz)")


        cbar = fig.colorbar(img, ax=ax)

        cbar.set_label("Intensity (dB)")


        plt.tight_layout()

        plt.savefig(

            spectrogram_path,
            dpi=DPI,
            bbox_inches="tight"

        )

        plt.close(fig)

        return spectrogram_path


    except Exception as e:

        print("Spectrogram save error:", e)

        return None