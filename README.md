# INFANT - Pediatric Leukemia Clinical Decision Support System

🧠 **INFANT** is an AI-powered Clinical Decision Support System (CDSS) designed to assist pediatric oncologists in managing and treating leukemia cases.  
It integrates clinical knowledge, patient records, imaging analysis, and AI-driven reasoning to provide evidence-based treatment recommendations.

---

## 📌 Features

- Multi-agent architecture with a central LLM (GPT) agent
- Patient-specific recommendations based on MRD, age, diagnosis
- Imaging AI for peripheral blood smear classification (simulated for now)
- Retrieval-Augmented Generation (RAG) from clinical guidelines
- Auto-generated downloadable PDF reports
- Doctor-friendly UI via Streamlit

---

## 🧰 Tech Stack

- Python 
- Streamlit
- OpenAI GPT-3.5 Turbo (via API)
- FAISS + SentenceTransformers (RAG)
- fpdf (PDF reports)
- PIL (Image handling)

---

## 🚀 How to Run

1. **Clone the repo**

```bash
git clone https://github.com/your-username/infant-cdss.git
cd infant-cdss

2. **Install dependencies**

```bash
pip install -r requirements.txt

3. **Set up your .env file**

4. **Run the app**
```bash
streamlit run app/main.py

## Project Structure
cdss_infant/
├── app/                  # Streamlit frontend
├── agents/               # LLM agent and strategy selector
├── tools/                # Imaging AI & clinical model tools
├── rag/                  # Knowledge base + FAISS retriever
├── patient_data/         # Patient info access module
├── utils/                # PDF report generator
├── data/                 # Sample documents and patient records
├── .env                  # API keys (excluded from Git)
├── requirements.txt
└── README.md

