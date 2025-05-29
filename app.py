import streamlit as st
import base64
import pandas as pd
import plotly.express as px
import PyPDF2
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# App configuration
st.set_page_config(page_title="CityPulse.AI", layout="wide")

# App title and branding
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🌆 CityPulse.AI</h1>
    <p style='text-align: center;'>Empowering Smarter Cities through Generative Intelligence</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📌 Navigation")
if st.sidebar.button("🤖 AI Chat Assistant", key="nav_chat"):
    st.session_state.current_page = "Chatbot"
if st.sidebar.button("📊 Usage Forecast", key="nav_forecast"):
    st.session_state.current_page = "Forecast"
if st.sidebar.button("📄 Smart Document Summary", key="nav_summary"):
    st.session_state.current_page = "Summary"
if st.sidebar.button("🧍 Citizen Guidance", key="nav_guidance"):
    st.session_state.current_page = "Guidance"

# Ensure session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Chatbot"

# Function to generate OpenAI response
def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except:
        return None

# Chatbot Page
if st.session_state.current_page == "Chatbot":
    st.markdown("""<h1 class='header'>🤖 AI Urban Assistant</h1>""", unsafe_allow_html=True)
    st.markdown("<div class='card'>Ask about urban planning, smart city solutions, or governance policies.</div>", unsafe_allow_html=True)
    user_input = st.text_area("Type your urban planning or city-related query here:")
    if st.button("Generate Insight"):
        if user_input:
            with st.spinner("Generating response..."):
                reply = generate_text(user_input)
                st.markdown(f"<div class='blue-card'><b>AI Insight:</b> {reply}</div>", unsafe_allow_html=True)

# Forecast Page
if st.session_state.current_page == "Forecast":
    st.markdown("<h1 class='header'>📊 Usage Forecast</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>Upload your city usage CSV to generate trend forecasts.</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "Month" in df.columns and "Usage" in df.columns:
            fig = px.line(df, x="Month", y="Usage", title="Monthly Usage Forecast", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("CSV must contain 'Month' and 'Usage' columns.")

# Smart Document Summary Page
if st.session_state.current_page == "Summary":
    st.markdown("<h1 class='header'>📄 Smart Document Summary</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>Upload a PDF file to get a summary of urban policies or reports.</div>", unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file is not None:
        text = extract_text_from_pdf(pdf_file)
        if text:
            with st.spinner("Summarizing..."):
                summary = generate_text(f"Summarize this urban document:\n\n{text[:3000]}")
                st.markdown(f"<div class='card'><b>Summary:</b><br>{summary}</div>", unsafe_allow_html=True)

# Citizen Guidance Page
if st.session_state.current_page == "Guidance":
    st.markdown("<h1 class='header'>🧍 Citizen Guidance</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>Interactive assistant for guidance on government schemes, local complaints, and public service options.</div>", unsafe_allow_html=True)
    guidance_question = st.text_input("Ask a guidance question:", key="guidance_input")
    if st.button("Get Guidance"):
        if guidance_question:
            with st.spinner("Analyzing citizen query..."):
                reply = generate_text(f"Provide actionable city-level guidance: {guidance_question}")
                st.markdown(f"<div class='blue-card'><b>Guidance:</b> {reply}</div>", unsafe_allow_html=True)

# Style
st.markdown("""
    <style>
        .header { font-size: 2.2em; color: #2E7D32; margin-bottom: 0.5em; }
        .card { background-color: #F0F4C3; padding: 1.2em; border-radius: 10px; }
        .blue-card { background-color: #E3F2FD; padding: 1em; border-left: 6px solid #42A5F5; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Sample CSV download for forecast
import io
def generate_sample_csv():
    sample_data = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr"], "Usage": [120, 135, 150, 165]})
    return sample_data.to_csv(index=False)

def get_csv_download_link(csv_text):
    b64 = base64.b64encode(csv_text.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="sample_usage.csv">📥 Download Sample CSV</a>'
