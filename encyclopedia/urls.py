from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("<str:name>", views.entrypage, name="entrypage"), 
    # path("new", views.new, name="new"),
    # path("edit", views.edit, name="edit"),
]
