from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import MinValueValidator
from main.models import Agent
from .choices import (
    ChatType,
    EditorObjectTypes,
    MessageObjectTypes,
    MessageObjectStatuses,
)


class Chat(models.Model):
    user_id = models.CharField(max_length=255, verbose_name=_("User ID"), editable=False)
    user_email = models.CharField(max_length=255, verbose_name=_("User email"))
    title = models.CharField(_("Title"), max_length=100, default="", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now_add=True)
    type = models.CharField(_("Type"), max_length=10, choices=ChatType.choices, default=ChatType.CHAT)
    # objs
    # messages

    def __str__(self):
        return f"{self._meta.model_name}[{self.pk}] {self.title}"

    class Meta:
        ordering = ['-date_updated']


class EditorObject(models.Model):
    task = models.ForeignKey(Chat, verbose_name=_("Chat"), related_name="objs", on_delete=models.CASCADE)
    content_type = models.CharField(_("Type"), max_length=10, choices=EditorObjectTypes.choices)
    content = models.TextField(_("Content"), default="", blank=True)
    file = models.FileField(_("File"), upload_to="jlab/editor/", null=True, blank=True)
    is_checked = models.BooleanField(_("Is checked?"), default=False)
    order = models.PositiveIntegerField(_("Order"), default=1, validators=[MinValueValidator(1)])
    inline_styles = models.JSONField(_("Inline styles"), blank=True, null=True)

    class Meta:
        ordering = ['pk']


class Message(models.Model):
    task = models.ForeignKey(Chat, verbose_name=_("Task"), related_name="messages", on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, verbose_name=_("Agent"), on_delete=models.CASCADE)
    is_answer = models.BooleanField(_("Is an answer by AI?"), blank=True, default=False)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    csat = models.BooleanField(_("CSAT Liked?"), null=True, blank=True, default=None)
    parameters = models.JSONField(_("Prompt parameters"), blank=True, null=True)
    # parent = models.ForeignKey("self", models.SET_NULL, verbose_name=_("Parent message (for AI replies)"), null=True, blank=True)
    # objs

    class Meta:
        ordering = ['date_created']


class MessageObject(models.Model):
    message = models.ForeignKey(Message, verbose_name=_("Message"), related_name="objs", on_delete=models.CASCADE)
    content_type = models.CharField(_("Type"), max_length=10, choices=MessageObjectTypes.choices)
    content = models.TextField(_("Content"), default="", blank=True)
    file = models.FileField(_("File"), upload_to="jlab/ai_chat/", null=True, blank=True)
    status = models.CharField(_("Status"), choices=MessageObjectStatuses.choices, default=MessageObjectStatuses.INITIAL, max_length=20)
    video_id = models.CharField(_("Synclab video ID"), null=True, default=None, blank=True, max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["video_id"], condition=models.Q(video_id__isnull=False), name="message-object--video_id-index"),
        ]
