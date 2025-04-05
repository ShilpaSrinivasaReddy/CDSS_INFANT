# clinical_model.py
# -----------------------------
# This file simulates a tool that finds similar patients based on clinical parameters.
# In the real version, this might query a database or use a trained model.
# Here, we return mock data.

class ClinicalModel:
    def get_similar_patients(self, patient_data):
        return [
            {"age": 5, "mrd": "10%", "outcome": "Recovered"},
            {"age": 6, "mrd": "12%", "outcome": "Switched to targeted therapy"}
        ]

