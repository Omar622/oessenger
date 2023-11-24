from enum import Enum
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rooms.models import Room, GroupRoom
from room_messages.models import Message

User = get_user_model()


class GroupRoomRole(Enum):
    """
    Enum for group room roles
    """

    OWNER = "Owner"
    MANAGER = "Manager"
    MEMBER = "Member"


class DmRoomMember(models.Model):
    """
    Dm room members model.
    """

    class Meta:
        """
        Provides metadata and configuration options for the DmRoomMember model.
        """

        verbose_name = _("DmRoomMember")
        verbose_name_plural = _("DmRoomMembers")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick name"), max_length=150,)
    last_seen_message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"Member: {self.nick_name}"


class GroupRoomMember(models.Model):
    """
    Group room members model.
    """

    class Meta:
        """
        Provides metadata and configuration options for the GroupRoomMember model.
        """

        verbose_name = _("GroupRoomMember")
        verbose_name_plural = _("GroupRoomMembers")

    ROLES = [
        ("ONR", GroupRoomRole.OWNER),
        ("MGR", GroupRoomRole.MANAGER),
        ("MBR", GroupRoomRole.MEMBER),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(GroupRoom, on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick name"), max_length=150)
    role = models.CharField(
        _("role"),
        max_length=3,
        choices=ROLES,
        default=str(GroupRoomRole.MEMBER))
    last_seen_message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"Member: {self.nick_name}"
