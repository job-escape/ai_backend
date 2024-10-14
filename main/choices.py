from django.db import models


class AgentTypes(models.TextChoices):
    TEXT = 'text', _('Text')
    VIDEO = 'video', _('Video')
    IMAGE = 'image', _('Image')