from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from common.forms import CommentForm
from common.mixins import UserIsOwnerMixin
from photos.forms import PhotoCreateForm, PhotoEditForm
from photos.models import Photo


class PhotoAddView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'photos/photo-add-page.html'
    success_url = reverse_lazy('home')


class PhotoDetailView(DetailView):
    model = Photo
    template_name = "photos/photo-details-page.html"

    def get_context_data(self, **kwargs):
        kwargs.update({
            "comments": self.object.comment_set.all(),
            "comment_form": CommentForm(),
        })
        return super().get_context_data(**kwargs)


class PhotoEditView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = "photos/photo-edit-page.html"
    success_url = reverse_lazy("home")


@login_required
def photo_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.get(pk=pk)

    if request.user.pk == photo.user.pk:
        photo.delete()
        return redirect('home')

    return HttpResponseForbidden()