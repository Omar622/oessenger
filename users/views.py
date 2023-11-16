from rest_framework import viewsets, mixins
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserViews(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """
    A viewset that provides CRUD operations for the User model.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
