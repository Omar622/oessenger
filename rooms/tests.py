import json
from django.forms import model_to_dict
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.factories import UserFactory
from .models import Room, GroupRoom
from .factories import GroupRoomFactory


def omit(data, keys):
    """
    Remove specific keys from a dictionary.
    """
    for key in keys:
        data.pop(key)
    return data


User = get_user_model()
client = Client()


def get_user():
    """
    create user and return it.
    """
    fake_user = UserFactory.build()
    user_instance = User(username=fake_user.username,
                         email=fake_user.email,)
    user_instance.set_password(fake_user.password)
    user_instance.save()
    return user_instance


def get_token(user):
    """
    creates token for given user and return it
    """
    return RefreshToken.for_user(user)


class RoomPostViewTests(TestCase):
    """
    This class contains test methods for creating group room.
    """

    def setUp(self):
        """
        Deletes all existing room and user objects before each test method is run
        """
        Room.objects.all().delete()
        User.objects.all().delete()

    def test_success(self):
        """
        Test method for successful room creation.
        """

        fake_group_room = omit(model_to_dict(GroupRoomFactory.build()),
                               ["id", "room_ptr", "picture_path"])

        fake_user = get_user()
        refresh = get_token(fake_user)

        print(fake_group_room)

        response = client.post(
            reverse("group_room-list"),
            data=fake_group_room,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),)  # type: ignore

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # check response body
        # response_data = json.loads(response.content.decode('utf-8'))
        # self.assertIsInstance(response_data["id"], int)
        # self.assertEqual(response_data["name"], fake_user.name)
        # self.assertEqual(response_data["description"], fake_user.description)
        # self.assertEqual(response_data["picture_path"], "")
        # self.assertEqual(response_data["number_of_participants"], 1)

        # # check db
        # user = GroupRoom.objects.get(pk=response_data["id"])
        # self.assertEqual(user.name, fake_user.name)
        # self.assertEqual(user.description, fake_user.description)
        # self.assertEqual(user.picture_path, '')


# class RoomGetViewTests(TestCase):
#     """
#     This class contains test methods for
#     """

#     def setUp(self):
#         """
#         Deletes all existing room and user objects before each test method is run
#         """
#         Room.objects.all().delete()
#         User.objects.all().delete()

#     def test_success_retrieve_group_room_info(self):
#         """
#         Test method for successful room info retrieving
#         """

#         # create user
#         fake_user = UserFactory.build()
#         user_instance = User(username=fake_user.username,
#                              email=fake_user.email,)
#         user_instance.set_password(fake_user.password)
#         user_instance.save()
#         refresh = RefreshToken.for_user(user_instance)

#         response = client.get(
#             reverse("group_room"),
#             HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
#         )
