from django.contrib import admin

from chat.models import (EditorObject, MessageObject, Message, Chat)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', )
    search_fields = ('pk', 'title', 'user_email')


admin.site.register(Message)
admin.site.register(MessageObject)
admin.site.register(EditorObject)
