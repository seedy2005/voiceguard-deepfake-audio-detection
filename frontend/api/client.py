import requests

API_URL = "http://127.0.0.1:5000"

def predict_audio(uploaded_file):
    try:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        response = requests.post(
            f"{API_URL}/predict",
            files=files
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}