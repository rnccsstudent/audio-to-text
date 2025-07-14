import streamlit as st
import whisper
import os
import tempfile
import requests

# Set Streamlit page config
st.set_page_config(page_title="Whisper Audio to Text", layout="centered")
st.title("🎙️ Whisper Audio-to-Text App")

# ----------------------------
# 🔧 FFMPEG Setup
# ----------------------------
FFMPEG_URL = "https://github.com/rnccsstudent/audio-to-text/releases/download/v1.0.0/ffmpeg"
FFMPEG_PATH = "/mnt/data/ffmpeg"  # Persistent storage on Render

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
            st.error(f"❌ Failed to download ffmpeg: {e}")
            st.stop()
    
    # Add /mnt/data to PATH
    os.environ["PATH"] = "/mnt/data" + os.pathsep + os.environ.get("PATH", "")

setup_ffmpeg()

# Confirm ffmpeg is working
if os.system("ffmpeg -version") != 0:
    st.error("❌ FFmpeg not working properly. Please check the binary.")
    st.stop()

# ----------------------------
# 📦 Load Whisper Model
# ----------------------------
@st.cache_resource
def load_model():
    try:
        model = whisper.load_model("tiny")
        return model
    except Exception as e:
        st.error(f"❌ Failed to load Whisper model: {e}")
        st.stop()

model = load_model()

# ----------------------------
# 📤 File Upload & Transcription
# ----------------------------
uploaded_file = st.file_uploader("📂 Upload an audio file", type=["mp3", "wav", "m4a", "flac", "ogg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-4:]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("🧠 Transcribing... Please wait ⏳")
    try:
        result = model.transcribe(tmp_path)
        st.success("✅ Transcription complete!")

        st.subheader("📝 Transcribed Text")
        st.text_area("Transcription", result["text"], height=300)

        st.download_button("📄 Download Transcription", result["text"], file_name="transcription.txt")
    except Exception as e:
        st.error(f"❌ Error during transcription: {e}")
