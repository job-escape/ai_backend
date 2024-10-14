import logging
import requests
import json
from tempfile import TemporaryFile
from urllib.request import urlopen
from django.conf import settings
from django.core.files import File
from django.utils import timezone
from main.models import (
    VideoAvatar,
    VideoAvatarTemplate,
)
from jlab.models import (
    MessageObject,
    MessageObjectStatuses,
    MessageObjectTypes,
    TaskMessage,
)
# from account.models import UserOnboarding
from main.utils import generate_image
from main.api import StreamAgentAPI
# from ai.celery import app
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

DUMMY_IMAGE_URL = "https://d7pqxnw01lpes.cloudfront.net/media/jlab_examples/example_4.webp"
DUMMY_VIDEO_URL = "https://d7pqxnw01lpes.cloudfront.net/media/jlab/avatars/video/video_310.mp4"
SYNERGIZER_STRENGTH = 1
if settings.DEBUG:
    WEBHOOK_URL = "https://stage.api.jobescape.me/ai_v2/synclab/"
else:
    WEBHOOK_URL = "https://api.jobescape.me/ai_v2/synclab/"



# def dummy_generate_video_task(msg_obj_id: int) -> bool:
#     try:
#         ai_msg_obj = MessageObject.objects.get(id=msg_obj_id)
#     except:  # pylint: disable=W0702
#         return False
#     with TemporaryFile("w+b") as tmp_file:
#         with urlopen(DUMMY_VIDEO_URL) as response:
#             tmp_file.write(response.read())
#         filename = f"stage_video_{ai_msg_obj.pk}.mp4" if settings.DEBUG else f"video_{ai_msg_obj.pk}.mp4"
#         ai_msg_obj.file.save(filename, File(tmp_file), save=False)
#     ai_msg_obj.status = MessageObjectStatuses.VIDEO_READY
#     ai_msg_obj.save()
#     return True

@api_view(['POST'])
def dummy_generate_video_task_view(request):
    """
    This endpoint handles the POST request to generate a dummy video 
    for the provided message object (msg_obj_id).
    
    Expected POST body:
    {
        "msg_obj_id": int
    }
    """
    try:
        # Parse the request body
        msg_obj_id = request.data.get('msg_obj_id')
        
        if not msg_obj_id:
            return Response({"error": "Invalid or missing msg_obj_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to fetch the MessageObject by its ID
        try:
            ai_msg_obj = MessageObject.objects.get(id=msg_obj_id)
        except MessageObject.DoesNotExist:
            return Response({"error": "MessageObject does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Generate the dummy video and save it to the MessageObject
        with TemporaryFile("w+b") as tmp_file:
            with urlopen(DUMMY_VIDEO_URL) as response:
                tmp_file.write(response.read())
            filename = f"stage_video_{ai_msg_obj.pk}.mp4" if settings.DEBUG else f"video_{ai_msg_obj.pk}.mp4"
            ai_msg_obj.file.save(filename, File(tmp_file), save=False)
        
        ai_msg_obj.status = MessageObjectStatuses.VIDEO_READY
        ai_msg_obj.save()

        return Response({"status": "Video generated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(f"Error generating video: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def dummy_generate_image_task_view(request):
    """
    This endpoint handles the POST request to generate a dummy image 
    for the provided message object (msg_obj_id).
    
    Expected POST body:
    {
        "msg_obj_id": int
    }
    """
    try:
        msg_obj_id = request.data.get('msg_obj_id')
        
        if not msg_obj_id:
            return Response({"error": "Invalid or missing msg_obj_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            ai_msg_obj = MessageObject.objects.get(id=msg_obj_id)
        except MessageObject.DoesNotExist:
            return Response({"error": "MessageObject does not exist"}, status=status.HTTP_404_NOT_FOUND)

        with TemporaryFile("w+b") as tmp_file:
            with urlopen(DUMMY_IMAGE_URL) as response:
                tmp_file.write(response.read())
            filename = f"stage_image_{ai_msg_obj.pk}.webp" if settings.DEBUG else f"image_{ai_msg_obj.pk}.webp"
            ai_msg_obj.file.save(filename, File(tmp_file), save=False)
        
        ai_msg_obj.status = MessageObjectStatuses.IMAGE_READY
        ai_msg_obj.save()

        return Response({"status": "Image generated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(f"Error generating image: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_video_task_view(request):
    """
    This API endpoint handles the POST request to generate a video for the provided
    user message and agent response (message object).

    Expected POST body:
    {
        "user_msg_id": int,
        "msg_obj_id": int,
        "avatar_id": int,
    }
    """
    exc_msg = "Generate video task: Aborting because "
    error = False
    
    try:
        user_msg_id = request.data.get('user_msg_id')
        msg_obj_id = request.data.get('msg_obj_id')
        avatar_id = request.data.get('avatar_id')
        
        if not user_msg_id or not msg_obj_id or not avatar_id:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ai_msg_obj = MessageObject.objects.get(id=msg_obj_id)
            user_message = TaskMessage.objects.get(id=user_msg_id)
            avatar = VideoAvatar.objects.get(id=avatar_id)
            avatar_template = VideoAvatarTemplate.objects.filter(avatar=avatar).first()
            
            if not avatar_template:
                logging.warning(f"{exc_msg} VideoAvatarTemplate does not exist! id={msg_obj_id}")
                error = True
            contents = user_message.objs.filter(content_type=MessageObjectTypes.TEXT).values_list("content", flat=True)
            if not contents or not any(contents):
                logging.warning(f"{exc_msg} user's Message does not contain non-empty text objects! user_msg_id={user_msg_id}")
                error = True

        except MessageObject.DoesNotExist:
            logging.warning(f"{exc_msg} related MessageObject does not exist! id={msg_obj_id}")
            error = True
        except TaskMessage.DoesNotExist:
            logging.warning(f"{exc_msg} user's Message does not exist! id={user_msg_id}")
            error = True
        except VideoAvatar.DoesNotExist:
            logging.error(f"{exc_msg} VideoAvatar does not exist! id={avatar_id}")
            error = True

        if error:
            MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.ERROR)
            return Response({"error": "Task failed due to missing resources or data"}, status=status.HTTP_400_BAD_REQUEST)

        if not ai_msg_obj.file:
            MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.ACCEPTED)
            text = "\n".join([i for i in contents if i])
            # Request Audio
            audio_url = f"https://api.elevenlabs.io/v1/text-to-speech/{avatar.el_id}"
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": avatar.stability,
                    "similarity_boost": avatar.similarity_boost,
                    "style": avatar.style,
                    "use_speaker_boost": avatar.use_speaker_boost,
                },
            }
            headers = {"Content-Type": "application/json", "xi-api-key": settings.ELEVENLABS_KEY}
            response = requests.post(audio_url, json=payload, headers=headers, timeout=settings.REQUESTS_TIMEOUT, stream=True)

            if response.status_code != 200:
                logging.warning(f"{exc_msg} ElevenLabs returned status_code={response.status_code}")
                MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.ERROR)
                return Response({"error": "Failed to generate audio"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            filename = f"stage_audio_{msg_obj_id}.mp3" if settings.DEBUG else f"audio_{msg_obj_id}.mp3"
            with TemporaryFile("w+b") as tmp_file:
                for chunk in response.iter_content(1024):
                    tmp_file.write(chunk)
                ai_msg_obj.file.save(filename, File(tmp_file), save=False)
                ai_msg_obj.status = MessageObjectStatuses.AUDIO_READY
                ai_msg_obj.save()

        # Request Video
        video_url = "https://api.synclabs.so/lipsync"
        payload = {
            "audioUrl": ai_msg_obj.file.url,
            "videoUrl": avatar_template.file.url,
            "model": "sync-1.6.0",
            "synergizerStrength": SYNERGIZER_STRENGTH,
            "webhookUrl": WEBHOOK_URL
        }
        headers = {"x-api-key": settings.SYNCLAB_KEY, "Content-Type": "application/json"}
        response = requests.post(video_url, json=payload, headers=headers, timeout=settings.REQUESTS_TIMEOUT)

        if response.status_code != 201:
            logging.warning(f"{exc_msg} SyncLab returned status_code={response.status_code}")
            MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.ERROR)
            return Response({"error": "Failed to generate video"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        ai_msg_obj.video_id = data["id"]
        ai_msg_obj.status = MessageObjectStatuses.AWAITING
        ai_msg_obj.save()

        return Response({"status": "Video generated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(f"{exc_msg} Exception: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_image_task_view(request):
    """
    This API endpoint handles the POST request to generate an image for the provided
    user message and agent response (message object).

    Expected POST body:
    {
        "user_msg_id": int,
        "msg_obj_id": int
    }
    """
    exc_msg = "Generate image task: Aborting because "
    error = True

    try:
        # Extract data from the request
        user_msg_id = request.data.get('user_msg_id')
        msg_obj_id = request.data.get('msg_obj_id')
        
        # Validate that required fields are present
        if not user_msg_id or not msg_obj_id:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch instances
        try:
            ai_msg_obj = MessageObject.objects.select_related("message__agent").get(id=msg_obj_id)
            ai_message = ai_msg_obj.message
            user_message = TaskMessage.objects.prefetch_related("objs").get(id=user_msg_id)

            # Fetch text content from user's TaskMessage
            prompt = StreamAgentAPI(ai_message).get_message_text_content(user_message)

            # Check if there's already an image associated with this message
            if ai_msg_obj.file:
                logging.warning("%s related MessageObject already has a file! id=%d", exc_msg, user_msg_id)
            else:
                error = False

        except MessageObject.DoesNotExist:
            logging.warning(f"{exc_msg} related MessageObject does not exist! id={msg_obj_id}")
            error = True
        except TaskMessage.DoesNotExist:
            logging.warning(f"{exc_msg} user's Message does not exist! id={user_msg_id}")
            error = True

        if error:
            MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.ERROR)
            return Response({"error": "Task failed due to missing resources or data"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the status to AWAITING if image generation hasn't already been done
        MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.AWAITING)

        # Generate image using external API (like OpenAI)
        try:
            images = generate_image(prompt, 1, "hd")
            assert images[0].url
        except Exception as exc:
            logging.warning(f"{exc_msg} openai failed to generate image! id={user_msg_id}; exception={str(exc)}")
            MessageObject.objects.filter(id=msg_obj_id).update(status=MessageObjectStatuses.ERROR)
            return Response({"error": "Failed to generate image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        with TemporaryFile("w+b") as tmp_file:
            with urlopen(images[0].url) as response:
                tmp_file.write(response.read())
            filename = f"stage_image_{ai_msg_obj.pk}.jpeg" if settings.DEBUG else f"image_{ai_msg_obj.pk}.jpeg"
            ai_msg_obj.file.save(filename, File(tmp_file), save=False)

        ai_msg_obj.status = MessageObjectStatuses.IMAGE_READY
        ai_msg_obj.save()

        return Response({"status": "Image generated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(f"{exc_msg} Exception: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

