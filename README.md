AI DEEPFAKE VOICE DETECTION SYSTEM 
A production-style AI security system for detecting synthetic (spoofed) 
speech using a Hybrid CNN + Transformer architecture. ------------------------------------------------------------------------ 
MODEL OVERVIEW -   CNN Layers extract local spectral patterns from Mel spectrograms -   Transformer Layers capture long-range temporal dependencies -   Softmax Output generates spoof probability -   Risk Policy Engine converts probability into security decisions ------------------------------------------------------------------------ 
FEATURES -   Audio Upload (WAV / MP3 / FLAC / OGG) -   Forensic Mel Spectrogram Visualization -   Dynamic Risk Meter -   3-Level Security Policy (ALLOW / CHALLENGE / BLOCK) -   Downloadable PDF Forensic Report -   GPU Acceleration (CUDA Supported) ------------------------------------------------------------------------ 
PROJECT STRUCTURE 
deepfake-voice-detection/ 
app.py -> Flask backend API checkpoints/ -> Trained model weights src/ -> Model & inference logic frontend/ -> Streamlit dashboard 
requirements.txt -> Dependencies ------------------------------------------------------------------------ 
INSTALLATION 
1.  Clone repository 
2.  Create virtual environment: python -m venv venv venv 
3.  Install dependencies: pip install -r requirements.txt ------------------------------------------------------------------------ 
RUNNING THE SYSTEM 
Start Backend: python app.py 
Runs on: http://localhost:5000 
Start Frontend: cd frontend streamlit run streamlit_app.py 
Runs on: http://localhost:8501 ------------------------------------------------------------------------ 
RISK POLICY 
0% – 30% -> ALLOW 30% – 70% -> CHALLENGE Above 70% -> BLOCK ------------------------------------------------------------------------ 
USE CASES -   Voice Authentication Security -   Banking IVR Fraud Detection -   Scam Call Detection -   Biometric System Hardening -   Audio Forensic Investigation ------------------------------------------------------------------------ 
Author: AI & Security Engineering Project 