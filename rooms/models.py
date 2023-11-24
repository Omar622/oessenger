from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    """
    Room model.
    """
    class Meta:
        """
        Provides metadata and configuration options for the Rooms model.
        """

        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    last_activity = models.DateTimeField(_("last activity"), auto_now=True)


class GroupRoom(Room):
    """
    Group Room model.
    """

    class Meta:
        """
        Provides metadata and configuration options for the Rooms model.
        """

        verbose_name = _("GroupRoom")
        verbose_name_plural = _("GroupRooms")

    name = models.CharField(_("name"), max_length=150)
    description = models.TextField(_("description"), blank=True)
    picture_path = models.CharField(
        _("picture path"), max_length=255, blank=True)

    def __str__(self):
        return f"Room: {self.name}"
