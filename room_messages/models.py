from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rooms.models import Room

User = get_user_model()


class Message(models.Model):
    """
    Message model.
    """

    class Meta:
        """
        Provides metadata and configuration options for the Message model.
        """

        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)


class TextMessage(Message):
    """
    TextMessage model.
    """

    class Meta:
        """
        Provides metadata and configuration options for the TextMessage model.
        """

        verbose_name = _("TextMessage")
        verbose_name_plural = _("TextMessages")

    content = models.TextField(_("content"), max_length=4096)
    is_edited = models.BooleanField(_("is edited"), default=False)

    def __str__(self):
        return f"Text Message: {self.content[:min(len(self.content), 30)]}"
