from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name='root'),
    path('<int:page>', views.main, name='root_paginate'),
    path('author/<int:_id>/', views.author, name='author'),
    path('new_quote/', views.new_quote, name='new_quote'),
    path('new_author/', views.new_author, name='new_author'),
    path('new_tag/', views.new_tag, name='new_tag'),
]