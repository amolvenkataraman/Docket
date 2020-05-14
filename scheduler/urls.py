from django.urls import include, path
from . import views

# URL patterns for main app
urlpatterns = [
    path("", views.index, name='index'),
    path("add/")
]
