import os
from dotenv import load_dotenv

load_dotenv()

ELEVEN_LABS_API_KEY = os.environ.get("ELEVEN_LABS_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")
