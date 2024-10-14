from typing import Any

from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from main.models import AgentTypes
from main.serializers import AgentTypeSerializer
from custom.custom_permissions import HasUnexpiredSubscription
from chat.models import (
    EditorObject,
    EditorObjectTypes,
    MessageObject,
    Chat,
    Message,
)
from chat.serializers import (
    MessageObjectListSerializer,
    MessageCreateSerializer,
    MessageCSATSerializer,
    ChatUpdateSerializer,
    ChatDetailSerializer,
    ChatMessagesSerializer,
    EditorObjectForChatSerializer,
)


class ChatViewSet(viewsets.GenericViewSet,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.RetrieveModelMixin):
    queryset = Chat.objects.all()
    permission_classes = [HasUnexpiredSubscription]
    request: Request

    def get_queryset(self):
        queryset = super().get_queryset().filter(user_id=self.request.user['user_id'])
        if self.action == 'retrieve':
            return queryset.prefetch_related('objs')\
                .annotate(videos=Count("objs", filter=Q(objs__content_type=EditorObjectTypes.VIDEO)))\
                .annotate(images=Count("objs", filter=Q(objs__content_type=EditorObjectTypes.IMAGE)))
        if self.action in ['update', 'partial_update']:
            return queryset.prefetch_related('objs')
        if self.action == 'messages_list':
            agent_type = self.request.query_params.get("type", AgentTypes.TEXT)
            prefetch = Prefetch("messages", Message.objects.filter(
                agent__type=agent_type).prefetch_related("agent", "objs"))
            return queryset.prefetch_related(prefetch)
        return queryset

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ChatUpdateSerializer
        if self.action == 'retrieve':
            return ChatDetailSerializer
        if self.action == 'messages_delete':
            return AgentTypeSerializer
        if self.action == 'messages':
            return MessageCreateSerializer
        if self.action == 'messages_list':
            return ChatMessagesSerializer
        if self.action == 'top_objects':
            return EditorObjectForChatSerializer
        return Serializer

    def perform_update(self, serializer):
        """Update the chat and set the date_updated field before saving."""
        serializer.validated_data['date_updated'] = timezone.now()
        super().perform_update(serializer)

    @ action(['post'], True)
    def messages(self, request: Request, pk=None):
        """Create user's Message with objects corresponding to it"""
        chat = self.get_object()
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        # self.__update_project_last_modified(task.project_id)
        message = ser.save(chat=chat)
        chat.date_updated = timezone.now()
        chat.save()
        ser2 = self.get_serializer(message)
        return Response(ser2.data, status=status.HTTP_201_CREATED)

    @ extend_schema(parameters=[AgentTypeSerializer])
    @ messages.mapping.delete
    def messages_delete(self, request: Request, pk=None):
        """Clear Ai Chat of a ProjectTask for a given agent type"""
        chat = self.get_object()
        ser = self.get_serializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        chat.messages.filter(agent__type=ser.data['type']).delete()
        chat.date_updated = timezone.now()
        chat.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @ extend_schema(parameters=[AgentTypeSerializer])
    @ messages.mapping.get
    def messages_list(self, request: Request, pk=None):
        """List user's ProjectTask's TaskMessages with objects corresponding to it"""
        ser = AgentTypeSerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        qs = self.get_queryset()
        chat = get_object_or_404(qs, pk=pk)
        ser = self.get_serializer(chat)
        return Response(ser.data)

    @ action(detail=True, pagination_class=None)
    def top_objects(self, request: Request, pk=None):
        """List user's ProjectTask's first 2 EditorObjects"""
        objs = EditorObject.objects.filter(chat_id=pk, order__in=[1, 2])
        ser = self.get_serializer(objs, many=True, read_only=True)
        return Response(ser.data)


class MessageViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = MessageCSATSerializer
    queryset = Message.objects.all()
    permission_classes = [HasUnexpiredSubscription]


class MessageObjectViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = MessageObjectListSerializer
    queryset = MessageObject.objects.all()
    permission_classes = [HasUnexpiredSubscription]
