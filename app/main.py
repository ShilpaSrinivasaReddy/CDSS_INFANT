# main.py
# -----------------------------
# This file contains the Streamlit UI for the INFANT chatbot.
# It collects a question and an optional image, retrieves patient info,
# and uses the LLMCoreAgent to provide clinical decision support.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agents.llm_agent import LLMCoreAgent
from agents.strategy_selector import StrategySelector
from tools.imaging_ai import ImagingAI
from tools.clinical_model import ClinicalModel
from patient_data.patient_info import get_patient_info

# Set Streamlit page title and layout
st.set_page_config(page_title="INFANT CDSS", layout="wide")
st.title("🧠 INFANT - Pediatric Leukemia Clinical Decision Support System")

# Ask the doctor for a clinical question
question = st.text_input("📋 Enter your clinical question:")

# Allow upload of a blood smear image (optional)
uploaded_image = st.file_uploader("📤 Upload a Peripheral Blood Smear Image (optional)", type=["png", "jpg", "jpeg"])

# Simulated patient selection
patient_id = st.selectbox("🩺 Select Patient ID", options=["P001", "P002"])

# When the doctor clicks submit
if st.button("🚀 Submit to INFANT"):
    # Step 1: Get patient record from simulated database
    patient_record = get_patient_info(patient_id)

    # Step 2: Prepare case data
    case_data = {
        "question": question,
        "image": uploaded_image.read() if uploaded_image else None,
        "patient_data": patient_record
    }

    # Step 3: Initialize tools and strategy agent
    tools = {
        "imaging": ImagingAI(),
        "clinical": ClinicalModel()
    }
    strategy_selector = StrategySelector()
    agent = LLMCoreAgent(strategy_selector, tools)

    # Step 4: Process case and show response
    with st.spinner("🧠 Thinking..."):
        response = agent.handle_case(case_data)

    st.subheader("📌 INFANT Response:")
    st.markdown(response)

    st.subheader("📁 Patient Info:")
    st.json(patient_record)
