# patient_info.py
# -----------------------------
# This file provides access to patient-specific clinical data.
# Currently, it loads mock patient data from a dictionary.
# Later, this can be replaced with real database or API access.

def get_patient_info(patient_id):
    # Simulated patient database
    mock_db = {
        "P001": {
            "age": 5,
            "diagnosis": "Intermediate-risk ALL",
            "mrd_day28": 10,
            "genetic_abnormalities": "None",
            "last_test": "Bone marrow aspiration on Mar 5, 2025",
            "status": "Partial response to initial chemo"
        },
        "P002": {
            "age": 7,
            "diagnosis": "High-risk ALL",
            "mrd_day28": 0,
            "genetic_abnormalities": "t(9;22)",
            "last_test": "Peripheral blood smear on Apr 1, 2025",
            "status": "Complete remission"
        }
    }

    return mock_db.get(patient_id, {"error": "Patient not found"})
