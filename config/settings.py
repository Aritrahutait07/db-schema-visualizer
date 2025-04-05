import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')  