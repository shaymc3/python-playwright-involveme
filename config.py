import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://app.involve.me")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")

LOGIN_URL = f"{BASE_URL}/login"
PROJECTS_URL = f"{BASE_URL}/projects"
TEMPLATES_URL = f"{BASE_URL}/templates"
EDITOR_PAGE = f"{BASE_URL}/editor"
