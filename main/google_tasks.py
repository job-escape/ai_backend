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

def create_generate_image_task(user_msg_id: int, msg_obj_id: int):
    """
    Creates a Google Cloud Task to trigger the generate_image_task_view
    endpoint via a POST request.

    :param user_msg_id: The user message ID to be sent in the request
    :param msg_obj_id: The agent message object ID to be sent in the request
    """
    client = tasks_v2.CloudTasksClient()

    project = settings.GCP_PROJECT_ID
    queue = 'generate-image-task'
    location = 'us-east1'
    parent = client.queue_path(project, location, queue)

    url = f"{settings.CLOUD_RUN_SERVICE_URL}/cloud_tasks/generate-image/"

    payload = {
        'user_msg_id': user_msg_id,
        'msg_obj_id': msg_obj_id,
    }

    payload_json = json.dumps(payload).encode()

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": payload_json,
        },
        "dispatch_deadline": {"seconds": 30 * 60}
    }

    response = client.create_task(request={"parent": parent, "task": task})
    return response


def create_generate_video_task(user_msg_id: int, msg_obj_id: int, avatar_id: int):
    """
    Creates a Google Cloud Task to trigger the generate_video_task_view
    endpoint via a POST request.

    :param user_msg_id: The user message ID to be sent in the request
    :param msg_obj_id: The agent message object ID to be sent in the request
    :param avatar_id: The avatar ID to be used in video generation
    """
    client = tasks_v2.CloudTasksClient()

    project = settings.GCP_PROJECT_ID
    queue = 'generate-video-task'
    location = 'us-east1'
    parent = client.queue_path(project, location, queue)

    url = f"{settings.CLOUD_RUN_SERVICE_URL}/cloud_tasks/generate-video/"

    payload = {
        'user_msg_id': user_msg_id,
        'msg_obj_id': msg_obj_id,
        'avatar_id': avatar_id
    }

    payload_json = json.dumps(payload).encode()

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": payload_json,
        },
        "dispatch_deadline": {"seconds": 30 * 60}
    }

    response = client.create_task(request={"parent": parent, "task": task})
    return response


def create_dummy_image_task(msg_obj_id: int):
    """
    Creates a Google Cloud Task to trigger the dummy_generate_image_task_view
    endpoint via a POST request.

    :param msg_obj_id: The agent message object ID to be sent in the request
    """
    client = tasks_v2.CloudTasksClient()

    project = settings.GCP_PROJECT_ID
    queue = 'dummy-generate-image-task'
    location = 'us-east1'
    parent = client.queue_path(project, location, queue)

    url = f"{settings.CLOUD_RUN_SERVICE_URL}/cloud_tasks/dummy-generate-image/"

    payload = {
        'msg_obj_id': msg_obj_id,
    }

    payload_json = json.dumps(payload).encode()

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": payload_json,
        },
        "dispatch_deadline": {"seconds": 30 * 60}
    }

    response = client.create_task(request={"parent": parent, "task": task})
    return response


def create_dummy_video_task(msg_obj_id: int):
    """
    Creates a Google Cloud Task to trigger the dummy_generate_video_task_view
    endpoint via a POST request.

    :param msg_obj_id: The agent message object ID to be sent in the request
    """
    client = tasks_v2.CloudTasksClient()

    project = settings.GCP_PROJECT_ID
    queue = 'dummy-generate-video-task'
    location = 'us-east1'
    parent = client.queue_path(project, location, queue)

    url = f"{settings.CLOUD_RUN_SERVICE_URL}/cloud_tasks/dummy-generate-video/"

    payload = {
        'msg_obj_id': msg_obj_id,
    }

    payload_json = json.dumps(payload).encode()

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": payload_json,
        },
        "dispatch_deadline": {"seconds": 30 * 60}
    }

    response = client.create_task(request={"parent": parent, "task": task})
    return response