from typing import Generator
import pytest
from faker import Faker
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
fake = Faker()


@pytest.fixture()
def api_client() -> Generator[APIClient, None, None]:
    """ api client without authentication """
    from rest_framework.test import APIClient
    yield APIClient()


@pytest.fixture()
def auth_api_client(db, api_client):
    """ APIClient with authentication factory """

    def make_auth_client(user: AbstractUser) -> APIClient:
        # api_client.force_login(user=user)

        # login
        api_client.force_authenticate(user=user)
        return api_client

    yield make_auth_client

    # logout on tear down
    api_client.force_authenticate(user=None)


@pytest.fixture()
def test_password():
    return "examples"


@pytest.fixture()
def create_user(db, django_user_model: AbstractUser, test_password: str):
    """ factory for creating users """
    def make_user(username, email, first_name, last_name) -> AbstractUser:
        new_user: AbstractUser = User.objects.create(username=username, email=email,
                                                     first_name=first_name, last_name=last_name)

        # assign password
        new_user.set_password(test_password)
        new_user.save()
        return new_user

    yield make_user


@pytest.fixture(scope="function")
def user_someone(create_user) -> AbstractUser:
    someone = create_user(username=fake.user_name(), email=fake.email(),
                          first_name=fake.first_name(), last_name=fake.last_name())

    return someone
