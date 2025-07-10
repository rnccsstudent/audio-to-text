import streamlit as st
import whisper
import os
import tempfile
import requests

st.write("App starting...")
st.write(f"PORT: {os.getenv('PORT')}")
# ----------------------------
# ⬇️ Download ffmpeg binary if not already cached
# ----------------------------

FFMPEG_URL = "https://github.com/rnccsstudent/audio-to-text/releases/download/v1.0.0/ffmpeg"
FFMPEG_PATH = "/mnt/data/ffmpeg"  # persistent storage on Render

def setup_ffmpeg():
    if not os.path.exists(FFMPEG_PATH):
        st.info("🔽 Downloading ffmpeg binary for first-time setup...")
        try:
            r = requests.get(FFMPEG_URL)
            r.raise_for_status()
            with open(FFMPEG_PATH, "wb") as f:
                f.write(r.content)
            os.chmod(FFMPEG_PATH, 0o755)  # Make it executable
            st.success("✅ ffmpeg downloaded and saved successfully.")
        except Exception as e:
            st.error(f"Failed to download ffmpeg: {e}")
            st.stop()

    # Add to PATH
    os.environ["PATH"] = "/mnt/data" + os.pathsep + os.environ.get("PATH", "")

setup_ffmpeg()

# ----------------------------
# ✅ Whisper App Starts Here
# ----------------------------

st.set_page_config(page_title="Whisper Audio to Text", layout="centered")
st.title("🎙️ Whisper Audio-to-Text App")

# Confirm ffmpeg is working
if not os.system("ffmpeg -version") == 0:
    st.error("❌ ffmpeg is not working. Please check the binary.")
    st.stop()

# Load model once
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

# Upload and Transcribe
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "flac", "ogg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("🧠 Transcribing... Please wait ⏳")
    result = model.transcribe(tmp_path)
    st.success("✅ Transcription complete!")

    st.subheader("📝 Transcribed Text")
    st.text_area("Output", result["text"], height=300)

    st.download_button("📄 Download Transcription", result["text"], file_name="transcription.txt")
