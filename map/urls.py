from django.urls import include, path
from . import views
from users import views as user_views

# URL patterns for main app
urlpatterns = [
    path("", views.map, name='map'),
    path("image", views.map_image, name='map_image'),
    path("add", views.add, name='add_loc'),
    path("register/", user_views.register_view, name='register'),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name='logout'),
]