from rest_framework import serializers
from interview_prep.models import (InterviewPrep, UserInterviewMessage,
                                   UserInterviewPrep)


class InterviewPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewPrep
        exclude = ['interview_sys_prompt', 'eval_sys_prompt']


class UserInterviewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterviewMessage
        exclude = ['user_interview', 'date_created']
        extra_kwargs = {
            "author_is_user": {"read_only": True},
        }


class UserInterviewPrepFullSerializer(serializers.ModelSerializer):
    messages = UserInterviewMessageSerializer(many=True, read_only=True)
    interview = InterviewPrepSerializer(read_only=True)

    class Meta:
        model = UserInterviewPrep
        fields = '__all__'


class InterviewPrepCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewPrep
        fields = ['title', 'initial_message']


class UserInterviewPrepCreateSerializer(serializers.ModelSerializer):
    interview = InterviewPrepCreateResponseSerializer(read_only=True)
    interview_id = serializers.IntegerField(required=True, allow_null=False)

    class Meta:
        model = UserInterviewPrep
        fields = ['interview', 'interview_id', 'id']


class UserInterviewPrepPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterviewPrep
        fields = ['user_grade', 'user_feedback']


class UserInterviewPrepEvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterviewPrep
        fields = ['ai_grade', 'ai_feedback', 'ai_strength', 'ai_weakness']
