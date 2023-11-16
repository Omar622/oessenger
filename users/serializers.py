from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for converting User model instances into Python data types,
    and vice versa. Provides validation and saving functionality for user data.
    """

    class Meta:
        """
        Metadata options for the UserSerializer class.
        """
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password',
                  'bio', 'last_activity', 'date_joined']

        extra_kwargs = {
            'id': {'read_only': True},
            'last_activity': {'read_only': True},
            'date_joined': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Creates a new user instance.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Updates an existing user instance.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        password = validated_data.get('password')

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
