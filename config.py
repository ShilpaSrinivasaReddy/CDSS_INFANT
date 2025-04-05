# config.py
# -----------------------------
# This file loads API keys from the .env file

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
