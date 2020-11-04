from django.urls import include, path
from . import views
from users import views as user_views

# URL patterns for main app
urlpatterns = [
    path("", views.chat, name='chat'),
]