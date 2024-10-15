from .core import (
    stage_generate_tasks, 
    prod_generate_tasks, 
    general_ai_tools, 
    gpt_secrets, 
    gcp_infos,
)
# AI SETTINGS
GPT_API_KEY = gpt_secrets.get('GPT_API_KEY')
GPT_MODEL_ENGINE = gpt_secrets.get('GPT_MODEL_ENGINE')
DALLE_MODEL_ENGINE = gpt_secrets.get('DALLE_MODEL_ENGINE')

# Gcloud project infos
GCP_PROJECT_ID = gcp_infos.get("GCP_PROJECT_ID")
GCP_LOCATION = gcp_infos.get("GCP_LOCATION")

# Generate tasks info for Google Cloud Tasks
# Stage
STAGE_AI_SERVICE_URL = stage_generate_tasks.get("STAGE_AI_SERVICE_URL")
STAGE_USERS_SERVICE_URL = stage_generate_tasks.get("STAGE_USERS_SERVICE_URL")
STAGE_QUEUE_UPDATE_ONBOARDING_TASK = stage_generate_tasks.get("STAGE_QUEUE_UPDATE_ONBOARDING_TASK")
STAGE_QUEUE_GENERATE_IMAGE_TASK = stage_generate_tasks.get("STAGE_QUEUE_GENERATE_IMAGE_TASK")
STAGE_QUEUE_GENERATE_VIDEO_TASK = stage_generate_tasks.get("STAGE_QUEUE_GENERATE_VIDEO_TASK")
STAGE_QUEUE_GENERATE_DUMMY_IMAGE_TASK = stage_generate_tasks.get("STAGE_QUEUE_GENERATE_DUMMY_IMAGE_TASK")
STAGE_QUEUE_GENERATE_DUMMY_VIDEO_TASK = stage_generate_tasks.get("STAGE_QUEUE_GENERATE_DUMMY_IMAGE_TASK")
# Prod
PROD_AI_SERVICE_URL = prod_generate_tasks.get("PROD_AI_SERVICE_URL") 
PROD_USERS_SERVICE_URL = prod_generate_tasks.get("PROD_USERS_SERVICE_URL")
PROD_QUEUE_UPDATE_ONBOARDING_TASK = prod_generate_tasks.get("PROD_QUEUE_UPDATE_ONBOARDING_TASK")
PROD_QUEUE_GENERATE_IMAGE_TASK = prod_generate_tasks.get("PROD_QUEUE_GENERATE_IMAGE_TASK")
PROD_QUEUE_GENERATE_VIDEO_TASK = prod_generate_tasks.get("PROD_QUEUE_GENERATE_VIDEO_TASK")
PROD_QUEUE_GENERATE_DUMMY_IMAGE_TASK = prod_generate_tasks.get("PROD_QUEUE_GENERATE_DUMMY_IMAGE_TASK")
PROD_QUEUE_GENERATE_DUMMY_VIDEO_TASK = prod_generate_tasks.get("PROD_QUEUE_GENERATE_DUMMY_IMAGE_TASK")

# Infos for image, video generating 
REQUESTS_TIMEOUT = 10
SYNCLAB_KEY = general_ai_tools.get("SYNCLAB_KEY")
ELEVENLABS_KEY = general_ai_tools.get("ELEVENLABS_KEY")
FRESHDESK_API_KEY = general_ai_tools.get("FRESHDESK_API_KEY")