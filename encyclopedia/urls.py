from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("encyclopedia/search.html", views.search, name="search"),
    path("encyclopedia/new.html", views.new_page, name="new_page"),
    path("encyclopedia/<str:name>/edit.html", views.edit, name="edit"),
    path("wiki/", views.random_page, name="random_page"),
]
