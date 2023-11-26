from pytz import utc
import factory
from factory.django import DjangoModelFactory
from .models import User


class UserFactory(DjangoModelFactory):
    """
    A Factory class for user model.
    """
    class Meta:
        """
        Configuration options for the UserFactory factory class.
        """
        model = User
        django_get_or_create = ('username', 'email',)

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('paragraph')
    picture_path = factory.Faker('file_path')
    last_login = factory.Faker('date_time_this_decade', tzinfo=utc)
