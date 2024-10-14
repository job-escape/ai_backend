import json

from openai.types.chat import ChatCompletion

from main.utils import generate_chat_completion
from main.base_api import BaseGenerationAPI
from interview_prep.models import UserInterviewMessage, UserInterviewPrep


class InterviewPrepAPI(BaseGenerationAPI):
    """
        API for streaming text questions for an interview preparation.
        Also allows to generate AI evaluation of an interview based on the content.
    """

    def __init__(self, user_interview: UserInterviewPrep) -> None:
        self.user_interview = user_interview

    # @override ( Requires Python version 3.12 )
    def get_user_prompt(self, *args, **kwargs) -> str:
        """Not used."""
        raise NotImplementedError()

    # @override ( Requires Python version 3.12 )
    def get_system_prompt(self, *args, is_eval: bool = False, **kwargs):
        interview = self.user_interview.interview
        assert interview, "UserInterviewPrep is not bound to any InterviewPrep!"
        return interview.eval_sys_prompt if is_eval else interview.interview_sys_prompt

    # @override ( Requires Python version 3.12 )
    def post_generate(self, full_content: str) -> None:
        UserInterviewMessage.objects.create(
            user_interview=self.user_interview,
            author_is_user=False,
            text=full_content
        )

    # @override ( Requires Python version 3.12 )
    def pre_generate(self, *args, **kwargs) -> None:
        for interview_message in self.user_interview.messages.all():  # type: ignore
            content = interview_message.text
            if content:
                role = "user" if interview_message.author_is_user else "assistant"
                self.append_message(content, role)

    def evaluate_interview(self):
        self.init_messages(is_eval=True)
        for interview_message in self.user_interview.messages.all():  # type: ignore
            content = interview_message.text
            if content:
                role = "user" if interview_message.author_is_user else "assistant"
                self.append_message(content, role)

        response = generate_chat_completion(self.messages, reply_json=True)
        assert isinstance(response, ChatCompletion)
        data = json.loads(response.choices[0].message.content or "{}")
        return data
