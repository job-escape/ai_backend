from django.contrib import admin

from interview_prep.models import (InterviewPrep, UserInterviewMessage,
                                   UserInterviewPrep)


@admin.register(InterviewPrep)
class InterviewPrepAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')


@admin.register(UserInterviewPrep)
class UserInterviewPrepAdmin(admin.ModelAdmin):
    list_display = ('pk', 'interview', 'user_email')
    search_fields = ('pk', 'user_email', )
    list_select_related = ('interview', )
    readonly_fields = ('user_email',)


@admin.register(UserInterviewMessage)
class UserInterviewMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_interview')
    list_select_related = ('user_interview',)