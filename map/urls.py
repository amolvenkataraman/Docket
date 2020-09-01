from django.urls import include, path
from . import views

# URL patterns for main app
urlpatterns = [
    path("", views.map, name='map'),
    path("image", views.map_image, name='map_image'),
]