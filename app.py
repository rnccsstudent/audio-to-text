import streamlit as st
import whisper
import os
import tempfile

if not os.system("ffmpeg -version") == 0:
    st.error("❌ ffmpeg is not installed. Whisper will not work.")

st.set_page_config(page_title="Whisper Audio to Text", layout="centered")
st.title("🎙️ Whisper Audio-to-Text App")

# Load model once
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "flac", "ogg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("Transcribing... Please wait ⏳")
    result = model.transcribe(tmp_path)
    st.success("✅ Transcription complete!")

    st.subheader("📝 Transcribed Text")
    st.text_area("Output", result["text"], height=300)

    # Downloadable text file
    st.download_button("📄 Download Transcription", result["text"], file_name="transcription.txt")
