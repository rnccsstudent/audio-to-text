import streamlit as st
import whisper
import os
import tempfile

# Set Streamlit page config
st.set_page_config(page_title="Whisper Audio to Text", layout="centered")
st.title("🎙️ Whisper Audio-to-Text App")

# ----------------------------
# 🔍 Check if FFmpeg is available
# ----------------------------
def check_ffmpeg():
    if os.system("ffmpeg -version") != 0:
        st.error("❌ FFmpeg is not available. Please ensure it's installed on the system.")
        st.stop()
    else:
        st.success("✅ FFmpeg is available.")

check_ffmpeg()

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
