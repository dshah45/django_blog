from django.contrib import admin
from django.conf.urls import url
from . import views
from django.urls import path, include
from .import views

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('', views.blogHome, name="blogHome"),
    path('<str:slug>', views.blogPost, name="blogPost"),
]
