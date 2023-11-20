from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserView(APIView):
    """
    A class representing a user view.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self):
        """get user from token instead of query path"""
        try:
            user = User.objects.get(id=self.request.user.id)  # type: ignore
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        """
        Return the list of permissions based on the request method.
        """
        if self.request.method in ["POST"]:
            return []
        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer},
        security=[],)
    def post(self, request, format=None):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve user data",
        responses={200: UserSerializer},)
    def get(self, request, format=None):
        """
        Retrieve a user object.
        """
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, format=None):
        """
        Update a user object.
        """
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request, format=None):
        """
        Update a user object.
        """
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete a user object.
        """
        user = self.get_object()
        user.delete()  # type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)
