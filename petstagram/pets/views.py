from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from common.forms import CommentForm
from common.mixins import UserIsOwnerMixin
from pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from pets.models import Pet


class PetAddView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetCreateForm
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})
    template_name = "pets/pet-add-page.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PetDetailsView(DetailView):
    model = Pet
    template_name = "pets/pet-details-page.html"
    slug_url_kwarg = "pet_slug"

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update({
            "comment_form": CommentForm(),
            "all_photos": self.object.photo_set.prefetch_related('tagged_pets', 'like_set').all(),
        })
        return super().get_context_data(**kwargs)


class PetEditView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Pet
    form_class = PetEditForm
    template_name = "pets/pet-edit-page.html"
    slug_url_kwarg = "pet_slug"

    def get_success_url(self) -> str:
        return reverse(
            "pet-details",
            kwargs={
                "username": self.kwargs.get("username"),
                "pet_slug": self.kwargs.get("pet_slug"),
            }
        )


class PetDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Pet
    template_name = "pets/pet-delete-page.html"
    success_url = reverse_lazy("profile-details", kwargs={"pk": 1})
    slug_url_kwarg = "pet_slug"
    form_class = PetDeleteForm

    def get_initial(self) -> dict:
        return self.object.__dict__

    # Option 1
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"data": self.get_initial()})
        return kwargs

    # Option 2
    # def post(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)
