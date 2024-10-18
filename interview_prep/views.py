import openai
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import StreamingHttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from custom.custom_exceptions import BadRequest
from custom.custom_renderers import ServerSentEventRenderer
from interview_prep.api import InterviewPrepAPI
from interview_prep.models import InterviewPrep, UserInterviewPrep
from interview_prep.serializers import (InterviewPrepSerializer,
                                        UserInterviewMessageSerializer,
                                        UserInterviewPrepCreateSerializer,
                                        UserInterviewPrepEvalSerializer,
                                        UserInterviewPrepFullSerializer,
                                        UserInterviewPrepPatchSerializer)
from interview_prep.speech_to_text import generate_transcription
from main.google_tasks import create_update_user_onboarding_task


class UserInterviewPrepViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """The viewset for working with the interviews (UserInterviewPreps)."""

    def get_queryset(self):
        qs = UserInterviewPrep.objects.filter(user_id=self.request.user.id)
        if self.action == 'retrieve':
            return qs.select_related('interview').prefetch_related('messages')
        if self.action == 'question':
            return qs.select_related('interview').prefetch_related('messages')
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserInterviewPrepFullSerializer
        if self.action == 'create':
            return UserInterviewPrepCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserInterviewPrepPatchSerializer
        if self.action == 'answer':
            return UserInterviewMessageSerializer
        if self.action == 'answer_audio':
            return UserInterviewMessageSerializer
        if self.action == 'evaluate':
            return UserInterviewPrepEvalSerializer
        return None

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, user_email=self.request.user.email)

    @extend_schema(request=None)
    @action(['post'], True)
    def evaluate(self, request: Request, pk=None):
        """The view evaluates a UserInterviewPrep using InterviewPrepAPI and returns evaluation data."""
        user_interview: UserInterviewPrep = self.get_object()
        if not user_interview.interview:
            raise BadRequest("UserInterviewPrep is not bound to any InterviewPrep!")
        data = InterviewPrepAPI(user_interview).evaluate_interview()
        user_interview.ai_grade = data.get("ai_grade", "Error.")
        user_interview.ai_feedback = data.get("ai_feedback", "Error.")
        user_interview.ai_strength = data.get("ai_strength", "Error.")
        user_interview.ai_weakness = data.get("ai_weakness", "Error.")
        user_interview.save()
        ser = self.get_serializer(user_interview)
        create_update_user_onboarding_task({"first_video": True}, str(request.auth))
        return Response(ser.data)

    @action(['post'], True)
    def answer(self, request: Request, pk=None):
        """Create UserInterviewMessage authored by the User with provided content."""
        user_interview = self.get_object()
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user_message = user_interview.messages.create(
            author_is_user=True,
            **ser.data
        )
        data = self.get_serializer(user_message).data
        return Response(data, status.HTTP_201_CREATED)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
    )
    @action(['post'], True, parser_classes=[MultiPartParser])
    def answer_audio(self, request: Request, pk=None):
        """
            Create UserInterviewMessage authored by the User based on provided audio track.
            The view uses `generate_transcription` util for transcripting the audio.
        """
        user_interview = self.get_object()
        if not request.FILES or not request.FILES.get("file", False):  # type: ignore
            raise BadRequest("File is required.")
        file: InMemoryUploadedFile = request.FILES['file']  # type: ignore
        try:
            transcription = generate_transcription(file)
        except openai.BadRequestError as exc:
            raise BadRequest(exc.body['message'] if exc.body else "Bad request") from exc  # type: ignore
        user_message = user_interview.messages.create(
            author_is_user=True,
            text=transcription
        )
        data = self.get_serializer(user_message).data
        return Response(data, status.HTTP_201_CREATED)

    @extend_schema(
        responses={
            (200, 'text/event-stream'): {
                'name': 'Empty',
                'type': 'string',
            }
        },
        request=None
    )
    @action(detail=True, renderer_classes=[ServerSentEventRenderer])
    def question(self, request: Request, pk=None):
        """
            Returns a Streaming HTTP Response rendered as Server-sent Event with text tokens.
            The view uses InterviewPrepAPI to generate text response.
            Raises Bad Request if requested UserInterviewPrep does not belong to any InterviewPrep.
        """
        user_interview: UserInterviewPrep = self.get_object()
        if not user_interview.interview:
            raise BadRequest("UserInterviewPrep is not bound to any InterviewPrep!")
        stream = InterviewPrepAPI(user_interview).get_text_stream()
        response = StreamingHttpResponse(stream, content_type="text/event-stream")
        response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
        response['Cache-Control'] = 'no-cache'  # Ensure clients don't cache the data
        return response


class InterviewPrepViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = InterviewPrep.objects.all()
    serializer_class = InterviewPrepSerializer
