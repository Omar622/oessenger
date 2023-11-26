import factory
from factory.django import DjangoModelFactory
from .models import Room, GroupRoom


class RoomFactory(DjangoModelFactory):
    """
    A Factory class for room model.
    """
    class Meta:
        """
        Configuration options for the RoomFactory factory class.
        """
        model = Room


class GroupRoomFactory(DjangoModelFactory):
    """
    A Factory class for group room model.
    """
    class Meta:
        """
        Configuration options for the GroupRoomFactory factory class.
        """
        model = GroupRoom

    name = factory.Faker('name')
    description = factory.Faker('paragraph')
    picture_path = factory.Faker('file_path')
