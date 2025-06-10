import os
from dotenv import load_dotenv
import praw

# Load .env from root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Debug print
print("Client ID:", os.getenv("REDDIT_CLIENT_ID"))

# Create Reddit instance
reddit = praw.Reddit(
    client_id=str(os.getenv("TybZ-JvFlWT9l5nwlIzuuw")),
    client_secret=str(os.getenv("938np3kTeC_YnGhw5_bHmrPNcHpHrw")),
    username=str(os.getenv("cronix472")),
    password=str(os.getenv("decsechacker47")),
    user_agent=str(os.getenv("DevRadar/0.1 by u/cronix472")),
)

# Confirm login
print(f"Logged in as: {reddit.user.me()}")
