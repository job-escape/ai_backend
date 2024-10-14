from .core import env

# AI SETTINGS
GPT_API_KEY = env('GPT_API_KEY')
GPT_MODEL_ENGINE = env('GPT_MODEL_ENGINE')
DALLE_MODEL_ENGINE = env('DALLE_MODEL_ENGINE')
USERS_SERVICE_URL = env("USERS_SERVICE_URL")
GCP_PROJECT_ID = env("GCP_PROJECT_ID")
GCP_LOCATION = env("GCP_LOCATION")
CLOUD_RUN_SERVICE_URL = env("CLOUD_RUN_SERVICE_URL")
ELEVENLABS_KEY = env("ELEVENLABS_KEY")
REQUESTS_TIMEOUT = 10
SYNCLAB_KEY = env("SYNCLAB_KEY")