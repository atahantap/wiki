from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage"),
    path("search", views.search, name="search"),
    path("<str:title>/editpage", views.editpage, name="editpage"),
    path("<str:entry_name>", views.entry, name="entry")
]
