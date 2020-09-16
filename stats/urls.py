from django.urls import include, path
from . import views

urlpatterns = [
    path("store", views.store_data, name='store_data'),
]