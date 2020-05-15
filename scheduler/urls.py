from django.urls import include, path
from . import views

# URL patterns for main app
urlpatterns = [
    path("", views.index, name='index'),
    path("add/", views.add, name='add'),
    path("enroll/", views.enroll, name='enroll'),
    path("stats/", views.stats, name='stats')
]
