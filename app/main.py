# main.py
# -----------------------------
# This file contains the Streamlit UI for the INFANT chatbot.
# It collects a question and an optional image, retrieves patient info,
# and uses the LLMCoreAgent to provide clinical decision support,
# and generates a downloadable PDF clinical summary report.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from PIL import Image
from agents.llm_agent import LLMCoreAgent
from agents.strategy_selector import StrategySelector
from tools.imaging_ai import ImagingAI
from tools.clinical_model import ClinicalModel
from patient_data.patient_info import get_patient_info
from utils.report_generator import generate_pdf  # ✅ NEW: PDF report generator

# Set Streamlit page title and layout
st.set_page_config(page_title="INFANT CDSS", layout="wide")
st.title("🧠 INFANT - Pediatric Leukemia Clinical Decision Support System")

# Step 1: Ask the doctor for a clinical question
question = st.text_input("📋 Enter your clinical question:")

# Step 2: Upload a blood smear image (optional)
uploaded_image = st.file_uploader("📤 Upload a Peripheral Blood Smear Image (optional)", type=["png", "jpg", "jpeg"])

# Step 3: Display the image in reduced size
if uploaded_image:
    image = Image.open(uploaded_image)
    resized_image = image.resize((350, 350))
    st.image(resized_image, caption="Peripheral Blood Smear", use_column_width=False)

# Step 4: Simulated patient selection
patient_id = st.selectbox("🩺 Select Patient ID", options=["P001", "P002"])

# Step 5: When the doctor clicks submit
if st.button("🚀 Submit to INFANT"):
    # Get patient record from simulated DB
    patient_record = get_patient_info(patient_id)

    # Prepare case data
    case_data = {
        "question": question,
        "image": uploaded_image.read() if uploaded_image else None,
        "patient_data": patient_record
    }

    # Initialize tools and agent
    tools = {
        "imaging": ImagingAI(),
        "clinical": ClinicalModel()
    }
    strategy_selector = StrategySelector()
    agent = LLMCoreAgent(strategy_selector, tools)

    # Run the analysis
    with st.spinner("🧠 INFANT is analyzing the case..."):
        response = agent.handle_case(case_data)

    # Display response
    st.subheader("📌 INFANT Response:")
    st.markdown(response)

    # Show patient info
    st.subheader("📁 Patient Info:")
    st.json(patient_record)

    # Generate tool summary (very basic)
    tool_summary = ""
    if uploaded_image:
        tool_summary += "- Imaging AI: Blood smear image analyzed.\n"
    if patient_record:
        tool_summary += "- Clinical Model: Compared with similar patients.\n"

    # Generate and offer the report as download
    pdf_path = generate_pdf(
        patient_info=patient_record,
        doctor_question=question,
        tool_summary=tool_summary,
        gpt_response=response
    )

    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📄 Download Clinical Summary Report (PDF)",
            data=file,
            file_name="INFANT_Clinical_Report.pdf",
            mime="application/pdf"
        )
