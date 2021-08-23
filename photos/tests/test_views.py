from django.urls import reverse

from faker import Faker

fake = Faker()


class TestPhoto:

    def test_create_photo(self, create_image, auth_api_client, user_someone):
        client = auth_api_client(user_someone)

        with open(create_image.name, 'rb') as im:
            url = reverse('photo-list')

            data = {
                "title": fake.name(),
                "image": im
            }

            resp = client.post(path=url, data=data, format='multipart')
            resp_data = resp.json()
            assert resp.status_code == 201