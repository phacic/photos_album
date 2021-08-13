import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import status
from django.urls import reverse

import pytest
from faker import Faker

fake = Faker()
JSON_CONTENT = "application/json"


@pytest.mark.django_db
class TestSignUp:

    def test_sign_up(self, api_client):
        """ test user can sign up"""
        url = reverse('sign_up')

        data = {
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        resp = api_client.post(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED

        # should contain token
        assert resp_data['token']

    # TODO test case where sign_up fails


@pytest.mark.django_db
class TestLogin:

    def test_login(self, api_client, user_someone, test_password):
        """ user should be able to login with correct password """

        url = reverse('login')
        data = {
            "username": user_someone.username,
            "password": test_password
        }
        resp = api_client.post(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK

        # should contain refresh and access token
        assert resp_data['access']
        assert resp_data['refresh']

    def test_login_with_wrong_password(self, api_client, user_someone):
        """ user should not be able to login with wrong password """

        url = reverse('login')
        data = {
            "username": user_someone.username,
            "password": "wrong-password"
        }
        resp = api_client.post(path=url, data=json.dumps(data), content_type=JSON_CONTENT)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUser:

    def test_user_update(self, auth_api_client, user_someone):
        """ users should be able to update their info """
        url = reverse('user-list') + f'{user_someone.id}/'
        client = auth_api_client(user=user_someone)

        new_first_name = fake.first_name()
        new_user_name = fake.user_name()

        data = {
            "first_name": new_first_name,
            "username": new_user_name
        }

        resp = client.patch(path=url, data=json.dumps(data), content_type=JSON_CONTENT)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert new_user_name == resp_data['username']
        assert new_first_name == resp_data['first_name']
