from django.conf.urls import url
from django.contrib import admin
from county import views

urlpatterns = [
    url('test/', views.test, name='test'),
    url('search/', views.search, name='search'),
]
