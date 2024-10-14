from django.db import transaction
from rest_framework import serializers

from main.models import Agent
from chat.models import (EditorObject, MessageObject, Chat, Message)

class EditorObjectForChatSerializer(serializers.ModelSerializer):
    delete = serializers.BooleanField(required=False, default=False, write_only=True)  # type: ignore
    file = serializers.URLField()

    class Meta:
        model = EditorObject
        exclude = ['chat']
        extra_kwargs = {
            'id': {'read_only': False},
        }


class ChatDetailSerializer(serializers.ModelSerializer):
    objs = EditorObjectForChatSerializer(many=True, read_only=True)
    videos = serializers.IntegerField()
    images = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = '__all__'


class ChatUpdateSerializer(serializers.ModelSerializer):
    objs = EditorObjectForChatSerializer(many=True, required=False)

    class Meta:
        model = Chat
        exclude = ['project']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def update(self, instance, validated_data: dict):
        objs_data: list[dict] = validated_data.pop('objs', [])
        updated = False
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            updated = True
        to_create = []
        to_update: list[dict] = []
        to_delete: list[int] = []
        for obj_data in objs_data:
            delete = obj_data.pop("delete", False)
            obj = EditorObject(**obj_data)
            if delete and obj.pk is not None:
                to_delete.append(obj.pk)
                continue
            if obj.pk is not None:
                to_update.append(obj_data)
            else:
                obj.chat = instance
                to_create.append(obj)
        with transaction.atomic():
            if updated:
                instance.save()
            if to_create:
                instance.objs.bulk_create(to_create)
            if to_update:
                # instance.objs.bulk_update(to_update, )
                for obj_data in to_update:
                    EditorObject.objects.filter(
                        pk=obj_data.pop("id"),
                        chat=instance
                    ).update(**obj_data)
            if to_delete:
                EditorObject.objects.filter(
                    pk__in=to_delete,
                    chat=instance
                ).delete()
        return instance


class MessageObjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageObject
        exclude = ['message']


class AgentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name']


class MessageListSerializer(serializers.ModelSerializer):
    agent = AgentShortSerializer(read_only=True)
    objs = MessageObjectListSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        exclude = ['task']


class ChatMessagesSerializer(serializers.ModelSerializer):
    messages = MessageListSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'messages']


class ChatShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


# class ProjectListSerializer(serializers.ModelSerializer):
#     tasks = ChatShortSerializer(many=True, read_only=True)

#     class Meta:
#         model = Project
#         fields = ['id', 'title', 'tasks', 'date_updated']


class ChatPreviewSerializer(serializers.ModelSerializer):
    objs = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="message_objects-detail")
    images = serializers.IntegerField()
    video = serializers.IntegerField()

    class Meta:
        model = Chat
        exclude = ['project']


# class ProjectRetrieveSerializer(serializers.ModelSerializer):
#     tasks = ChatPreviewSerializer(many=True, read_only=True)

#     class Meta:
#         model = Project
#         fields = ['id', 'title', 'tasks']


# class ProjectFullSerializer(serializers.ModelSerializer):
#     tasks = ChatShortSerializer(many=True, read_only=True)

#     class Meta:
#         model = Project
#         fields = '__all__'


# class ProjectShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'title']
#         extra_kwargs = {
#             'id': {'read_only': True}
#         }


# class ProjectCreateRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['deliverables', 'description', 'goal', 'duration']


# class ProjectCreateResponseSerializer(ProjectShortSerializer):
#     tasks = ChatShortSerializer(many=True, read_only=True)

#     class Meta:
#         model = Project
#         fields = ProjectShortSerializer.Meta.fields + ['tasks']


class MessageObjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageObject
        exclude = ['message', 'status', 'video_id']
        extra_kwargs = {
            'id': {'read_only': True}
        }

class MessageCSATSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['csat']

class MessageCreateSerializer(serializers.ModelSerializer):
    objs = MessageObjectCreateSerializer(many=True)

    class Meta:
        model = Message
        exclude = ['task']
        extra_kwargs = {
            'id': {'read_only': True},
            'is_answer': {'read_only': True}
        }

    def create(self, validated_data):
        objs_data: list[dict] = validated_data.pop('objs', [])
        instance = super().create(validated_data)
        to_create = []

        for obj_data in objs_data:
            obj = MessageObject(**obj_data)
            obj.message = instance
            to_create.append(obj)
        if to_create:
            instance.objs.bulk_create(to_create)
        return instance
