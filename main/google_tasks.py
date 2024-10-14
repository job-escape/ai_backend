import google.auth
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from datetime import datetime, timedelta
import json
from django.conf import settings

def create_update_user_onboarding_task(fields, token):
    """Creates a task to update the user's onboarding status."""
    
    client = tasks_v2.CloudTasksClient()

    parent = client.queue_path(settings.GCP_PROJECT_ID, settings.GCP_LOCATION, 'testing-queue')

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.PATCH,
            "url": f"{settings.USERS_SERVICE_URL}/users/onboarding/",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            "body": json.dumps(fields).encode()
        }
    }

    client.create_task(parent=parent, task=task)