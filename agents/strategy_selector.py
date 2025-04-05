# strategy_selector.py
# -----------------------------
# This file defines the StrategySelector and strategies.
# GeneralQueryStrategy now uses GPT to handle open-ended questions.

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class StrategySelector:
    def select(self, case_data):
        if case_data.get("image"):
            return PeripheralSmearAnalysisStrategy()
        elif "treatment" in case_data.get("question", "").lower():
            return TreatmentPersonalizationStrategy()
        else:
            return GeneralQueryStrategy()

class PeripheralSmearAnalysisStrategy:
    def execute(self, case_data, tools):
        image_result = tools['imaging'].analyze_blood_smear(case_data["image"])
        return f"Imaging Result: {image_result}"

class TreatmentPersonalizationStrategy:
    def execute(self, case_data, tools):
        patient_data = case_data.get("patient_data", {})
        match = tools['clinical'].get_similar_patients(patient_data)
        return f"Similar Cases Found: {match}"

# ✅ NEW: General questions are handled using OpenAI GPT
class GeneralQueryStrategy:
    def execute(self, case_data, tools):
        try:
            user_question = case_data.get("question", "")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant who explains pediatric leukemia topics clearly."},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=500,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error from GPT: {str(e)}"
