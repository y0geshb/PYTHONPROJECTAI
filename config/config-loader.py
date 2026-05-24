import os
from config.environments import ensure_environment_loaded, get_api_mode

ENV = os.getenv("ENV", "qa")
API_MODE = ensure_environment_loaded()
BASE_URL = os.getenv("API_BASE_URL")
LOGIN_ENDPOINT = os.getenv("API_LOGIN_ENDPOINT")

USER_EMAIL = os.getenv("API_USER_EMAIL")
USER_PASSWORD = os.getenv("API_USER_PASSWORD")