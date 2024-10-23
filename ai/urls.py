from django.urls import path, include
from main.views import (
    AiViewSet
)
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from drf_spectacular import views as SchemaViews
from main.views import (
    AiViewSet,
    AgentViewSet,
)
from chat.views import (
    ChatViewSet,
    MessageViewSet,
    MessageObjectViewSet,
)
from interview_prep.views import (
    UserInterviewPrepViewSet,
    InterviewPrepViewSet,
)
from main.cloud_task_endpoints import (
    dummy_generate_image_task_view,
    dummy_generate_video_task_view,
    generate_image_task_view,
    generate_video_task_view,
)

router = routers.SimpleRouter()

router.register(r'ai', AiViewSet, 'ai')
router.register(r'ai/agents', AgentViewSet, 'ai/agents')

router.register(r'chats', ChatViewSet, 'chats')
router.register(r'messages', MessageViewSet, 'messages')
router.register(r'message_objects', MessageObjectViewSet, 'message_objects')

router.register(r'interview_prep', InterviewPrepViewSet, 'interview_prep')
router.register(r'user_interview_prep', UserInterviewPrepViewSet, 'user_interview_prep')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # download
    path('schema/', SchemaViews.SpectacularAPIView.as_view(), name='schema'),
    # schema with swagger UI
    path('schema/swagger-ui/',
         SchemaViews.SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # schema with redoc UI
    path('schema/redoc/',
         SchemaViews.SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('cloud_tasks/generate-image/', generate_image_task_view, name='google_task_generate_image'),
    path('cloud_tasks/generate-video/', generate_video_task_view, name='google_task_generate_video'),
    path('cloud_tasks/dummy-generate-image/', dummy_generate_image_task_view, name='google_task_dummy_generate_image'),
    path('cloud_tasks/dummy-generate-video/', dummy_generate_video_task_view, name='google_task_dummy_generate_video'),
]
