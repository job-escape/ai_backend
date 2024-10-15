from google.cloud import tasks_v2
import json
from django.conf import settings

def create_update_user_onboarding_task(fields, token):
    """Creates a task to update the user's onboarding status."""
    
    client = tasks_v2.CloudTasksClient()
    if settings.STAGE:
        queue = settings.STAGE_QUEUE_UPDATE_ONBOARDING_TASK
        url = f"{settings.STAGE_USERS_SERVICE_URL}/users/onboarding/"
    else:
        queue = settings.PROD_QUEUE_UPDATE_ONBOARDING_TASK
        url = f"{settings.PROD_USERS_SERVICE_URL}/users/onboarding/"
    parent = client.queue_path(settings.GCP_PROJECT_ID, settings.GCP_LOCATION, queue)
    

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.PATCH,
            "url": url,
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
    if settings.STAGE:
        queue = settings.STAGE_QUEUE_GENERATE_IMAGE_TASK
        url = f"{settings.STAGE_AI_SERVICE_URL}/cloud_tasks/generate-image/"
    else:
        queue = settings.PROD_QUEUE_GENERATE_IMAGE_TASK
        url = f"{settings.PROD_AI_SERVICE_URL}/cloud_tasks/generate-image/"
    parent = client.queue_path(settings.GCP_PROJECT_ID, settings.GCP_LOCATION, queue)

    payload = {
        'user_msg_id': user_msg_id,
        'msg_obj_id': msg_obj_id,
    }

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(payload).encode(),
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

    if settings.STAGE:
        queue = settings.STAGE_QUEUE_GENERATE_VIDEO_TASK
        url = f"{settings.STAGE_AI_SERVICE_URL}/cloud_tasks/generate-video/"
    else:
        queue = settings.PROD_QUEUE_GENERATE_VIDEO_TASK
        url = f"{settings.PROD_AI_SERVICE_URL}/cloud_tasks/generate-video/"
    parent = client.queue_path(settings.GCP_PROJECT_ID, settings.GCP_LOCATION, queue)

    payload = {
        'user_msg_id': user_msg_id,
        'msg_obj_id': msg_obj_id,
        'avatar_id': avatar_id
    }

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(payload).encode(),
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
    
    if settings.STAGE:
        queue = settings.STAGE_QUEUE_GENERATE_DUMMY_IMAGE_TASK
        url = f"{settings.STAGE_AI_SERVICE_URL}/cloud_tasks/dummy-generate-image/"
    else:
        queue = settings.PROD_QUEUE_GENERATE_DUMMY_IMAGE_TASK
        url = f"{settings.PROD_AI_SERVICE_URL}/cloud_tasks/dummy-generate-image/"
        
    parent = client.queue_path(settings.GCP_PROJECT_ID, settings.GCP_LOCATION, queue)

    payload = {
        'msg_obj_id': msg_obj_id,
    }

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(payload).encode(),
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

    if settings.STAGE:
        queue = settings.STAGE_QUEUE_GENERATE_DUMMY_VIDEO_TASK
        url = f"{settings.STAGE_AI_SERVICE_URL}/cloud_tasks/dummy-generate-video/"
    else:
        queue = settings.PROD_QUEUE_GENERATE_DUMMY_VIDEO_TASK
        url = f"{settings.PROD_AI_SERVICE_URL}/cloud_tasks/dummy-generate-video/"
        
    parent = client.queue_path(settings.GCP_PROJECT_ID, settings.GCP_LOCATION, queue)

    payload = {
        'msg_obj_id': msg_obj_id,
    }

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(payload).encode(),
        },
        "dispatch_deadline": {"seconds": 30 * 60}
    }

    response = client.create_task(request={"parent": parent, "task": task})
    return response