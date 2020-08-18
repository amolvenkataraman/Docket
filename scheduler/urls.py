from django.urls import include, path
from . import views

# URL patterns for main app
urlpatterns = [
    path("", views.index, name='index'),
    path("data/", views.get_data, name='data'),
    path("add/", views.add, name='add'),
    path("enroll/", views.enroll, name='enroll'),
    path("class/", views.class_, name='class_'),
    path("stats/", views.stats, name='stats'),
]
