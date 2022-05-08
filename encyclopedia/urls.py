from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:name>", views.entrypage, name="entrypage"),
    path("<str:name>/edit", views.edit, name="edit"),
]
