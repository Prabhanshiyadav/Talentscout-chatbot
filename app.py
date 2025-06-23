# app.py

import streamlit as st
from utils import generate_tech_questions, extract_text_from_pdf, convert_audio_to_text
from prompts import greeting_prompt, end_prompt
import json
from utils import generate_tech_questions, extract_text_from_pdf

st.set_page_config(page_title="TalentScout Hiring Assistant")

if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.data = {}

st.title("🤖 TalentScout Hiring Assistant")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Resume Text", resume_text, height=200)

audio_file = st.file_uploader("Upload your voice answer (.wav)", type=["wav"])
if audio_file is not None:
    text_response = convert_audio_to_text(audio_file)
    st.text_area("Voice Answer Transcription", text_response)

# Initialize all session state variables
if "step" not in st.session_state:
    st.session_state.step = "start"
if "tech_stack" not in st.session_state:
    st.session_state.tech_stack = ""
if "full_name" not in st.session_state:
    st.session_state.full_name = ""
if "data" not in st.session_state:
    st.session_state.data = {}


if st.session_state.step == "start":
    st.write(greeting_prompt())
    if st.button("Start Interview"):
        st.session_state.step = "info"

elif st.session_state.step == "info":
    st.subheader("Candidate Information")
    st.session_state.data["full_name"] = st.text_input("Full Name")
    st.session_state.data["email"] = st.text_input("Email Address")
    st.session_state.data["phone"] = st.text_input("Phone Number")
    st.session_state.data["experience"] = st.slider("Years of Experience", 0, 30, 1)
    st.session_state.data["position"] = st.text_input("Desired Position(s)")
    st.session_state.data["location"] = st.text_input("Current Location")
    st.session_state.data["tech_stack"] = st.text_area("Your Tech Stack")

    uploaded_pdf = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded_pdf:
        st.session_state.data["pdf_text"] = extract_text_from_pdf(uploaded_pdf)
        st.success("✅ Resume content extracted")

    voice_bytes = st.file_uploader("Upload your voice (WAV)", type=["wav"])
    if voice_bytes:
        st.session_state.data["voice_input"] = convert_audio_to_text(voice_bytes)
        st.success("✅ Voice input transcribed")

    if st.button("Generate Questions"):
        st.session_state.step = "questions"

elif st.session_state.step == "questions":
    st.subheader("🧠 Technical Questions Based on Your Tech Stack")

    questions = generate_tech_questions(st.session_state.tech_stack)

    st.session_state.questions = questions  # Save in session if needed

    for i, question in enumerate(questions, start=1):
        st.text_area(f"Q{i}: {question}", key=f"answer_{i}")

    if st.button("End Conversation"):
        st.session_state.step = "end"


elif st.session_state.step == "end":
    full_name = st.session_state.data.get("full_name", "Candidate")
    st.success(end_prompt(full_name))

    st.write("📋 Summary of Your Responses:")
    st.json(st.session_state.data)

    if st.download_button("Download JSON Report", json.dumps(st.session_state.data, indent=2),
                          file_name="talentscout_summary.json"):
        st.success("✅ Downloaded JSON successfully!")
