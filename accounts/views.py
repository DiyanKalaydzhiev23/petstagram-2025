from urllib.request import Request
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from accounts.forms import AppUserCreationForm, ProfileEditForm
from accounts.models import Profile

UserModel = get_user_model()


class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Note: Signal for profile creation

        if response.status_code in [301, 302]:
            login(self.request, self.object)

        return response


def profile_details_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile-details-page.html')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_likes'] = self.object.user.photo_set.annotate(
            num_likes=Count('like')
        ).aggregate(total_likes=Sum('num_likes')).get('total_likes') or 0
        context['pets_count'] = self.object.user.pet_set.count()
        context['photos_count'] = self.object.user.photo_set.count()

        return context

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self) -> str:
        return reverse(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )


def app_user_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = UserModel.objects.get(pk=pk)

    if request.user.is_authenticated and request.user.pk == user.pk:
        if request.method == "POST":
            user.delete()
            return redirect('home')
    else:
        return HttpResponseForbidden()

    return render(request, 'accounts/profile-delete-page.html')
