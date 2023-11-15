from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """
    A custom user model that extends the default user model.
    """

    bio = models.TextField(_("bio"))
    picture_path = models.CharField(
        _("picture path"), max_length=255, blank=True, null=True)
    last_activity = models.DateTimeField(_("last_activity"), default=timezone.now)

    def __str__(self):
        return f"User: {self.username}"
