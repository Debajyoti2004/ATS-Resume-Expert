from dotenv import load_dotenv
import os
import io
import base64
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:        
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]
        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format='JPEG')
        img_bytes_arr = img_bytes_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes_arr).decode()
            }
        ]
        
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI Design
st.set_page_config(page_title="ATS Resume Expert", layout="centered")

st.markdown("""
    <style>
        body { background-color: #121212; color: #fff; }
        .main-header { text-align: center; font-size: 3em; color: #f72585; text-shadow: 0 0 10px #f72585; }
        .sub-header { text-align: center; font-size: 1.5em; color: #ffb703; }
        .stButton>button { width: 100%; margin-top: 10px; background: linear-gradient(145deg, #8338ec, #3a86ff); color: white; border: none; border-radius: 10px; padding: 10px; }
        .uploaded-file { font-size: 1.2em; color: #06d6a0; }
        .response-container { background: #1b1b1b; padding: 20px; border-radius: 15px; border: 1px solid #8338ec; box-shadow: 0 0 15px #8338ec; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>ATS Resume Expert 🎧</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Boost your resume to match job descriptions seamlessly 🎤</div>", unsafe_allow_html=True)

# Job Description input
st.subheader("Enter Job Description")
input_text = st.text_area("", placeholder="Paste the job description here...")

# Resume upload
st.subheader("Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("", type=["pdf"])
if uploaded_file is not None:
    st.markdown("<div class='uploaded-file'>✅ PDF Uploaded Successfully!</div>", unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button("💡 Evaluate Resume")
with col2:
    submit2 = st.button("🚀 Improve Skills")
with col3:
    submit3 = st.button("📊 Match Score")

# Prompts
input_prompt1 = """You are an HR guru with a tech twist, skilled in AI, Web Dev, and Data Analysis. Review this resume versus the job description—spotlight the strengths and call out the gaps."""

input_prompt2 = """You're a career wizard! Identify skill gaps and offer hot tips—think tools, certs, and projects that'll skyrocket the applicant's profile."""

input_prompt3 = """You are an ATS specialist. Calculate the percentage match between the resume and job description. Consider skills, experience, and job-specific keywords. Provide a match score out of 100 with an explanation."""

# Responses
if submit1 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input=input_text, pdf_content=pdf_content, prompt=input_prompt1)
    st.markdown("<div class='response-container'>", unsafe_allow_html=True)
    st.subheader("🎯 Resume Evaluation")
    st.write(response)
    st.markdown("</div>", unsafe_allow_html=True)

elif submit2 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input=input_text, pdf_content=pdf_content, prompt=input_prompt2)
    st.markdown("<div class='response-container'>", unsafe_allow_html=True)
    st.subheader("🔥 Skill Improvement Suggestions")
    st.write(response)
    st.markdown("</div>", unsafe_allow_html=True)

elif submit3 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input=input_text, pdf_content=pdf_content, prompt=input_prompt3)
    st.markdown("<div class='response-container'>", unsafe_allow_html=True)
    st.subheader("📊 Match Percentage")
    st.write(response)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    if uploaded_file is None and (submit1 or submit2 or submit3):
        st.error("🚨 Please upload a PDF first.")
