from django.urls import include, path
from . import views
from users import views as user_views

# URL patterns for main app
urlpatterns = [
    path("", views.map, name='map'),
    path("image", views.map_image, name='map_image'),
    path("add", views.add, name='add_loc'),
]