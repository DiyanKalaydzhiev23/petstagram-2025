from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from pets.models import Pet
from photos.validators import FileSizeValidator


UserModel = get_user_model()


class Photo(models.Model):
    photo = CloudinaryField(
        resource_type='image',
        validators=[
            FileSizeValidator(5),
        ],
    )

    description = models.TextField(
        max_length=300,
        validators=[
            MinLengthValidator(10),
        ],
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    tagged_pets = models.ManyToManyField(
        to=Pet,
        blank=True,
    )

    date_of_publication = models.DateField(
        auto_now=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )