from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import MaxValueValidator, MinValueValidator


class InterviewPrep(models.Model):
    title = models.CharField(_("Title"), max_length=50, blank=True)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    icon = models.ImageField(_("Icon"), upload_to='interview_prep/images/', max_length=100, null=True, blank=True)
    interview_sys_prompt = models.TextField(_("Interview system prompt"))
    eval_sys_prompt = models.TextField(_("Evaluation system prompt"))
    initial_message = models.CharField(_("Initial message"), max_length=300)

    def __str__(self):
        return f"{self._meta.model_name}[{self.pk}] {self.title}"


class UserInterviewPrep(models.Model):
    interview = models.ForeignKey(InterviewPrep, verbose_name=_("Interview prep"), on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.CharField(max_length=255, verbose_name=_("User ID"), editable=False)
    user_email = models.CharField(max_length=255, verbose_name=_("User email"))
    ai_grade = models.IntegerField(_("AI grade"), validators=[MinValueValidator(0), MaxValueValidator(5)], default=0, blank=True)
    ai_feedback = models.CharField(_("AI feedback"), max_length=455, blank=True)
    ai_strength = models.CharField(_("AI strength"), max_length=400, blank=True)
    ai_weakness = models.CharField(_("AI weakness"), max_length=400, blank=True)
    user_grade = models.IntegerField(_("User grade"), validators=[MinValueValidator(0), MaxValueValidator(5)], default=0, blank=True)
    user_feedback = models.CharField(_("Description"), max_length=255, blank=True)
    # messages


class UserInterviewMessage(models.Model):
    user_interview = models.ForeignKey(UserInterviewPrep, verbose_name=_("User interview prep"), related_name="messages", on_delete=models.CASCADE)
    author_is_user = models.BooleanField(_("Author is user?"), default=False, blank=True)
    text = models.TextField(_("Text"), blank=True)
    date_created = models.DateTimeField(_("Date created"), auto_now=True)

    class Meta:
        ordering = ['date_created']
