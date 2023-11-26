from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GroupRoom
from .serializers import GroupRoomSerializer
from .permissions import IsGroupRoomMember, IsGroupRoomOwner


class GroupRoomViewSet(viewsets.GenericViewSet,
                       viewsets.mixins.CreateModelMixin,
                       viewsets.mixins.UpdateModelMixin,
                       viewsets.mixins.RetrieveModelMixin):
    """
    Generic viewset for GroupRoom
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsGroupRoomOwner]
        else:
            permission_classes = [IsAuthenticated, IsGroupRoomMember]
        return [permission() for permission in permission_classes]

    queryset = GroupRoom.objects.all()
    serializer_class = GroupRoomSerializer
