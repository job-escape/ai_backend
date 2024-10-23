from django.db import models
from django.utils.translation import gettext_lazy as _

class ChatType(models.TextChoices):
    CHAT = 'chat', _('Chat')
    PLAYGROUND = 'playground', _('Playground')
    MENTOR = 'mentor', _("Mentor")


class MessageObjectTypes(models.TextChoices):
    TEXT = 'text', _('Text')
    IMAGE = 'image', _('Image')
    VIDEO = 'video', _('Video')
    # AUDIO = 'audio', _('Audio')
    QUOTE = 'quote', _('Quote')


class EditorObjectTypes(models.TextChoices):
    TEXT = 'text', _('Text')
    IMAGE = 'image', _('Image')
    VIDEO = 'video', _('Video')
    AUDIO = 'audio', _('Audio')
    CHECKBOX = 'checkbox', _('Checkbox')
    H1 = 'h1', _('Header 1')
    H2 = 'h2', _('Header 2')
    H3 = 'h3', _('Header 3')
    OL = 'ol', _('Ordered list')
    UL = 'ul', _('Unordered list')


class MessageObjectStatuses(models.TextChoices):
    INITIAL = 'initial', _('Initial')
    ACCEPTED = 'accepted', _('Accepted')
    ERROR = 'error', _('Error')
    RETRY = 'retry', _('Retry')
    AUDIO_READY = 'audio_ready', _('Audio Ready')
    VIDEO_READY = 'video_ready', _('Video Ready')
    IMAGE_READY = 'image_ready', _('Image Ready')
    AWAITING = 'awaiting', _('Awaiting')