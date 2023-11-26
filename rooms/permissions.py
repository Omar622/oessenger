
from rest_framework.permissions import BasePermission
from members.models import GroupRoomMember, GroupRoomRole


class IsGroupRoomMember(BasePermission):
    """
    Allows access only to group room members.
    """

    def has_permission(self, request, view):
        return GroupRoomMember.objects.filter(user=request.user).exists()


class IsGroupRoomOwner(BasePermission):
    """
    Allows access only to group room members.
    """

    def has_permission(self, request, view):

        try:
            member = GroupRoomMember.objects.get(user=request.user)
            return member.role == GroupRoomRole.OWNER
        except err:
            return False
