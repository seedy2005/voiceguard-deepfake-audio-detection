# 🎙️ VoiceGuard AI

### Deepfake Audio Detection System (Real vs Fake Voice)

> 🔐 Detect AI-generated voice scams (vishing) using deep learning

---

## 🧠 Overview

VoiceGuard is an AI-powered system that detects whether an audio sample is **real or deepfake**.

It uses a **hybrid deep learning architecture** combining:

* 📊 CNN (Mel Spectrogram)
* 🔁 Transformer (Raw Audio Waveform)

This allows the model to capture both:

* Frequency-based anomalies
* Temporal inconsistencies

---

## ⚙️ How It Works

1. 🎧 Upload an audio file
2. 🔍 Extract features:

   * Mel Spectrogram (for CNN)
   * Raw waveform (for Transformer)
3. 🧠 Model processes both inputs
4. 📊 Output:

   * Prediction → `Real` or `Fake`
   * Confidence score

---

## 🏗️ Tech Stack

* 🐍 Python
* 🔥 PyTorch
* 🎵 Librosa
* 🌐 Flask (Backend API)
* 🎨 HTML, CSS, JavaScript (Frontend)

---

## 📂 Project Structure

```
.
├── app.py                 # Flask backend
├── requirements.txt
├── README.md
│
├── src/
│   ├── model.py
│   ├── model_cnn.py
│   ├── predict.py
│   ├── mel_extractor.py
│   ├── train.py
│   └── ...
│
├── templates/             # HTML files
├── static/                # CSS, JS
│
└── samples/               # Demo audio files (optional)
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/voiceguard-ai.git
cd voiceguard-ai
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the app

```bash
python app.py
```

---

### 4️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 📊 Model Architecture

* CNN → Extracts spectral features from Mel spectrogram
* Transformer → Learns temporal patterns from raw waveform
* Fusion Layer → Combines both for final prediction

---

## 🎯 Use Cases

* 📞 Detect voice phishing (vishing)
* 🏦 Banking & fraud prevention
* 🎙️ Fake celebrity voice detection
* 🛡️ Cybersecurity systems

---

## ⚠️ Notes

* Model weights (`.pt`) are not included due to size
* You can add your trained model inside:

```
models/
```

---

## 📌 Future Improvements

* 🔊 Real-time audio detection
* 🌐 Deploy as web service
* 📱 Mobile app integration
* 🎯 Improve accuracy with larger datasets

---

## 🤝 Contributing

Feel free to fork, improve, and submit a pull request!

---

## 👨‍💻 Author

**Your Name**
AI & ML Engineer | Cybersecurity Enthusiast

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
