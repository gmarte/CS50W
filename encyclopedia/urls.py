from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("add/<str:title>", views.add, name="add"),
    path("search/", views.search, name="search"),
    path("random/", views.random, name="random")
]
