from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from photos.models import Photo

UserModel = get_user_model()

class TestPhotoDeleteView(TestCase):
    def setUp(self):
        self.credentials_author = {
            "email": "myemail@gmail.com",
            "password": "12admin34"
        }
        self.credentials_visitor = {
            "email": "myemail2@gmail.com",
            "password": "12admin34"
        }

        self.user_author = UserModel.objects.create_user(
            **self.credentials_author,
        )
        self.user_visitor = UserModel.objects.create_user(
            **self.credentials_visitor,
        )

        self.photo = Photo.objects.create(
            photo="photo.png",
            description="Test description here",
            location="test",
            user=self.user_author
        )

        self.client.login(
            **self.credentials_author,
        )

    def test_delete_photo_as_author_expect_success(self):
        response = self.client.post(
            path=reverse('delete-photo', kwargs={"pk": self.photo.pk},),
        )

        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertRedirects(response, reverse('home'))

    def test_delete_photo_as_visitor_expect_http_forbidden(self):
        self.client.login(**self.credentials_visitor)

        response = self.client.post(
            path=reverse('delete-photo', kwargs={"pk": self.photo.pk},),
        )

        self.assertTrue(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertEqual(response.status_code, 403)








