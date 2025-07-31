from django import forms

from common.mixins import ReadOnlyMixin
from pets.models import Pet


class PetBaseForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "date_of_birth", "personal_photo"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    'placeholder': 'Pet Name',
                },
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            "personal_photo": forms.TextInput(
                attrs={
                    "placeholder": "Link to Image",
                }
            )
        }

        labels = {
            "name": "Pet name",
            "date_of_birth": "Date of birth",
            "personal_photo": "Link to image",
        }


class PetCreateForm(PetBaseForm):
    ...


class PetEditForm(PetBaseForm):
    ...


class PetDeleteForm(ReadOnlyMixin, PetBaseForm):
    ...
