# report_generator.py
# -----------------------------
# This file generates a structured PDF report for the INFANT system
# using patient info, tool outputs, and the final GPT response.

from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "INFANT - Clinical Summary Report", ln=True, align="C")
        self.ln(10)

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, content)
        self.ln(5)

def generate_pdf(patient_info, doctor_question, tool_summary, gpt_response):
    pdf = PDFReport()
    pdf.add_page()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 8, f"Generated on: {now}", ln=True)
    pdf.ln(5)

    pdf.add_section(" Patient Information", str(patient_info))
    pdf.add_section(" Doctor's Question", doctor_question)
    pdf.add_section(" Tool Outputs", tool_summary)
    pdf.add_section(" INFANT's Response", gpt_response)

    output_path = "report_output.pdf"
    pdf.output(output_path)
    return output_path
