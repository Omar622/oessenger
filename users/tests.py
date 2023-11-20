import json
from django.test import TestCase, Client
from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .factories import UserFactory


def omit(data, keys):
    """
    Remove specific keys from a dictionary.
    """
    for key in keys:
        data.pop(key)
    return data


client = Client()


class UserPostViewTests(TestCase):
    """
    This class contains test methods for creating a user through
    a POST request to an API endpoint. It covers different scenarios such as
    successful creation, repeated username or email, and missing required fields.
    """

    def setUp(self):
        """
        Deletes all existing user objects before each test method is run.
        """
        User.objects.all().delete()

    def test_success_with_required_attrs_only(self):
        """
        Test method for successful user creation.
        """
        fake_user = omit(model_to_dict(UserFactory.build()), [
                         "id", "last_name", "bio", "picture_path", "last_login"])
        response = client.post(reverse("user"), data=fake_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check response body
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data["id"], int)
        self.assertEqual(response_data["last_name"], "")
        self.assertEqual(response_data["bio"], "")
        self.assertEqual(response_data["picture_path"], "")
        self.assertEqual(response_data["username"], fake_user["username"])
        self.assertEqual(response_data["first_name"], fake_user["first_name"])
        self.assertEqual(response_data["email"], fake_user["email"])

        # check db
        user = User.objects.get(username=fake_user["username"])
        self.assertEqual(user.email, fake_user["email"])
        self.assertEqual(user.first_name, fake_user["first_name"])

    def test_success_with_all_attrs(self):
        """
        Test method for successful user creation.
        """
        fake_user = omit(model_to_dict(UserFactory.build()), ["id"])

        response = client.post(reverse("user"), data=fake_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check response body
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data["id"], int)
        self.assertEqual(response_data["username"], fake_user["username"])
        self.assertEqual(response_data["first_name"], fake_user["first_name"])
        self.assertEqual(response_data["email"], fake_user["email"])
        self.assertEqual(response_data["last_name"], fake_user["last_name"])
        self.assertEqual(response_data["bio"], fake_user["bio"])
        self.assertEqual(response_data["picture_path"], fake_user["picture_path"])

        # check db
        user = User.objects.get(username=fake_user["username"])
        self.assertEqual(fake_user["email"], user.email)
        self.assertEqual(fake_user["first_name"], user.first_name)
        self.assertEqual(fake_user["last_name"], user.last_name)
        self.assertEqual(fake_user["bio"], user.bio)

    def test_failure_with_repeated_username(self):
        """
        Test method for user creation with repeated username.
        """
        fake_user = UserFactory()
        repeated_username_fake_user = omit(model_to_dict(
            UserFactory.build(username=fake_user.username)), ["id"])

        response = client.post(reverse("user"), data=repeated_username_fake_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_with_repeated_email(self):
        """
        Test method for user creation with repeated email.
        """
        fake_user = UserFactory()
        repeated_email_fake_user = omit(model_to_dict(
            UserFactory.build(email=fake_user.email)), ["id"])

        response = client.post(reverse("user"), data=repeated_email_fake_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_with_missing_username(self):
        """
        Test method for user creation with missing username.
        """
        fake_user = omit(model_to_dict(UserFactory.build()), ["id", "username"])

        response = client.post(reverse("user"), data=fake_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_with_missing_email(self):
        """
        Test method for user creation with missing email.
        """
        fake_user = omit(model_to_dict(UserFactory.build()), ["id", "email"])

        response = client.post(reverse("user"), data=fake_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_with_missing_password(self):
        """
        Test method for user creation with missing password.
        """
        fake_user = omit(model_to_dict(UserFactory.build()), ["id", "password"])

        response = client.post(reverse("user"), data=fake_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_with_missing_first_name(self):
        """
        Test method for user creation with missing first name.
        """
        fake_user = omit(model_to_dict(UserFactory.build()), ["id", "first_name"])

        response = client.post(reverse("user"), data=fake_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDeleteViewTests(TestCase):
    """
    A test class for testing the functionality of deleting a user.
    """

    def setUp(self):
        """
        Deletes all existing user objects before each test method is run.
        """
        User.objects.all().delete()

    def test_success(self):
        """
        Tests the successful deletion of a user.
        """
        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email, password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)

        response = client.delete(
            reverse("user"),
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))   # type: ignore

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_failure_invalid_token(self):
        """
        Tests the failure case when an invalid token is provided.
        """
        response = client.delete(
            reverse("user"),
            HTTP_AUTHORIZATION='Bearer not-found-token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_failure_no_token(self):
        """
        Tests the failure case when no token is provided.
        """
        response = client.delete(reverse("user"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserGetViewTests(TestCase):
    """
    A test case class for testing the successful retrieval of user data.
    """

    def setUp(self):
        """
        Deletes all existing user objects before each test method is run.
        """
        User.objects.all().delete()

    def test_success(self):
        """
        Test the successful scenario of retrieving user data.
        """
        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email, password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)

        response = client.get(
            reverse("user"),
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))   # type: ignore

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check response body
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data["id"], int)
        self.assertIsInstance(response_data["last_activity"], str)
        self.assertIsInstance(response_data["date_joined"], str)
        self.assertEqual(response_data["username"], fake_user.username)
        self.assertEqual(response_data["first_name"], fake_user.first_name)
        self.assertEqual(response_data["email"], fake_user.email)
        self.assertEqual(response_data["last_name"], fake_user.last_name)
        self.assertEqual(response_data["bio"], fake_user.bio)
        self.assertEqual(response_data["picture_path"], fake_user.picture_path)

    def test_failure_invalid_token(self):
        """
        Tests the failure case when an invalid token is provided.
        """
        response = client.get(
            reverse("user"),
            HTTP_AUTHORIZATION='Bearer not-found-token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_failure_no_token(self):
        """
        Tests the failure case when no token is provided.
        """
        response = client.get(reverse("user"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserPutViewTests(TestCase):
    """
    A test case class for testing the successful updating of user data.
    """

    def setUp(self):
        """
        Deletes all existing user objects before each test method is run.
        """
        User.objects.all().delete()

    def test_success(self):
        """
        A method that tests the success case of updating a user's information.
        """
        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email,
                             password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)
        updated_fake_user = model_to_dict(UserFactory.build())

        response = client.put(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check response body
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data["id"], int)
        self.assertEqual(response_data["username"], updated_fake_user["username"])
        self.assertEqual(response_data["first_name"], updated_fake_user["first_name"])
        self.assertEqual(response_data["email"], updated_fake_user["email"])
        self.assertEqual(response_data["last_name"], updated_fake_user["last_name"])
        self.assertEqual(response_data["bio"], updated_fake_user["bio"])
        self.assertEqual(response_data["picture_path"],
                         updated_fake_user["picture_path"])

        # check db
        user = User.objects.get(id=fake_user.id)  # type: ignore
        self.assertEqual(user.username, updated_fake_user["username"])
        self.assertEqual(user.email, updated_fake_user["email"])
        self.assertEqual(user.first_name, updated_fake_user["first_name"])
        self.assertEqual(user.last_name, updated_fake_user["last_name"])
        self.assertEqual(user.bio, updated_fake_user["bio"])
        self.assertEqual(user.picture_path, updated_fake_user["picture_path"])

    def test_failure_repeated_username(self):
        """
        Tests the failure case when updating user with existing username.
        """
        existing_user = UserFactory()

        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email,
                             password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)
        updated_fake_user = model_to_dict(
            UserFactory.build(username=existing_user.username))

        response = client.put(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_repeated_email(self):
        """
        Tests the failure case when updating user with existing email.
        """
        existing_user = UserFactory()

        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email,
                             password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)
        updated_fake_user = model_to_dict(
            UserFactory.build(email=existing_user.email))

        response = client.put(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_invalid_token(self):
        """
        Tests the failure case when an invalid token is provided.
        """
        updated_fake_user = model_to_dict(UserFactory.build())

        response = client.put(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer not-found-token',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_failure_no_token(self):
        """
        Tests the failure case when no token is provided.
        """
        updated_fake_user = model_to_dict(UserFactory.build())

        response = client.put(
            reverse("user"),
            data=updated_fake_user,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UsePatchViewTests(TestCase):
    """
    A test case class for testing the successful updating of user data.
    """

    def setUp(self):
        """
        Deletes all existing user objects before each test method is run.
        """
        User.objects.all().delete()

    def test_success_update_username(self):
        """
        Tests the success case of updating a username.
        """
        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email,
                             password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)
        updated_fake_user = {"username": "updated_username"}

        response = client.patch(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check response body
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data["id"], int)
        self.assertEqual(response_data["username"], updated_fake_user["username"])
        self.assertEqual(response_data["first_name"], fake_user.first_name)
        self.assertEqual(response_data["email"], fake_user.email)
        self.assertEqual(response_data["last_name"], fake_user.last_name)
        self.assertEqual(response_data["bio"], fake_user.bio)
        self.assertEqual(response_data["picture_path"],
                         fake_user.picture_path)

        # check db
        user = User.objects.get(id=fake_user.id)  # type: ignore
        self.assertEqual(user.username, updated_fake_user["username"])
        self.assertEqual(user.email, fake_user.email)
        self.assertEqual(user.first_name, fake_user.first_name)
        self.assertEqual(user.last_name, fake_user.last_name)
        self.assertEqual(user.bio, fake_user.bio)
        self.assertEqual(user.picture_path, fake_user.picture_path)

    def test_failure_repeated_username(self):
        """
        Tests the failure case when updating user with existing username.
        """
        existing_user = UserFactory()

        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email,
                             password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)
        updated_fake_user = {"username": existing_user.username}

        response = client.patch(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_repeated_email(self):
        """
        Tests the failure case when updating user with existing email.
        """
        existing_user = UserFactory()

        fake_user = UserFactory()
        user_instance = User(id=fake_user.id,  # type: ignore
                             username=fake_user.username,
                             email=fake_user.email,
                             password=fake_user.password)
        refresh = RefreshToken.for_user(user_instance)
        updated_fake_user = {"email": existing_user.email}

        response = client.patch(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token),  # type: ignore
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_invalid_token(self):
        """
        Tests the failure case when an invalid token is provided.
        """
        updated_fake_user = {"first_name": "updated_first_name"}

        response = client.patch(
            reverse("user"),
            data=updated_fake_user,
            HTTP_AUTHORIZATION='Bearer not-found-token',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_failure_no_token(self):
        """
        Tests the failure case when no token is provided.
        """
        updated_fake_user = {"first_name": "updated_first_name"}

        response = client.patch(
            reverse("user"),
            data=updated_fake_user,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
