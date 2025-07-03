from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, resolve_url
from django.template.context_processors import request
from django.views.generic import ListView
from pyperclip import copy

from common.forms import CommentForm, SearchForm
from common.models import Like
from photos.models import Photo


class HomePageView(ListView):
    model = Photo
    template_name = "common/home-page.html"
    context_object_name = "all_photos"
    paginate_by = 5
    
    def get_context_data(self, *, object_list: list=None, **kwargs) -> dict:
        kwargs.update({
            "comment_form": CommentForm(),
            "search_form": SearchForm(),
        })
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('text')

        if pet_name:
            queryset = queryset.prefetch_related('tagged_pets', 'like_set').filter(
                tagged_pets__name__icontains=pet_name
            )

        return queryset


def home_page_view(request: HttpRequest) -> HttpResponse:
    comment_form = CommentForm()
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        all_photos = Photo.objects.prefetch_related('tagged_pets', 'like_set').filter(
            tagged_pets__name__icontains=search_form.cleaned_data.get('text', '')
        )
    else:
        all_photos = Photo.objects.prefetch_related('tagged_pets', 'like_set').all()

    context = {
        "all_photos": all_photos,
        "comment_form": comment_form,
        "search_form": search_form,
    }

    return render(request, 'common/home-page.html', context)


def like(request: HttpRequest, photo_id: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_id,
            user=request.user,
        )

    return redirect(request.META.get('HTTP_REFERER') + f"#{photo_id}")


def share(request: HttpRequest, photo_id: int) -> HttpResponse:
    # pip install pyperclip
    # This will only work locally
    copy(request.META.get('HTTP_HOST') + resolve_url('photo-details', photo_id))

    return redirect(request.META.get('HTTP_REFERER') + f"#{photo_id}")


def add_comment(request: HttpRequest, photo_id: int) -> HttpResponse:
    form = CommentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.to_photo = Photo.objects.get(pk=photo_id)
        comment.user = request.user
        comment.save()

    return redirect(request.META.get('HTTP_REFERER') + f"#{photo_id}")
