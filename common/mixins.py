from django.contrib.auth.mixins import UserPassesTestMixin


class ReadOnlyMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True


class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.pk == self.get_object().user.pk
