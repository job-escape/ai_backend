"""
URL configuration for ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from main.views import (
    AiViewSet
)
from rest_framework import routers
from django.contrib import admin
from django.urls import path
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

router.register(r'ai', AiViewSet)
router.register(r'main/agents', AgentViewSet)

router.register(r'chats', ChatViewSet, 'chats')
router.register(r'messages', MessageViewSet, 'messages')
router.register(r'message_objects', MessageObjectViewSet, 'message_objects')

router.register(r'interview_prep', InterviewPrepViewSet)
router.register(r'user_interview_prep', UserInterviewPrepViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('cloud_tasks/generate-image/', generate_image_task_view, name='google_task_generate_image'),
    path('cloud_tasks/generate-video/', generate_video_task_view, name='google_task_generate_video'),
    path('cloud_tasks/dummy-generate-image/', dummy_generate_image_task_view, name='google_task_dummy_generate_image'),
    path('cloud_tasks/dummy-generate-video/', dummy_generate_video_task_view, name='google_task_dummy_generate_video'),
]
