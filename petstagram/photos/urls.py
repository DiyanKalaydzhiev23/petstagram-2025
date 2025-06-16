from django.urls import path, include
from photos import views

urlpatterns = [
    path('add/', views.PhotoAddView.as_view(), name='add-photo'),
    path('<int:pk>/', include([
        path('', views.PhotoDetailView.as_view(), name='photo-details'),
        path('edit/', views.PhotoEditView.as_view(), name='edit-photo'),
        path('delete/', views.photo_delete_view, name='delete-photo'),
    ])),
]
