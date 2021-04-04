from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home , name = 'home'),
    path('uploader/', views.uploader , name = 'uploader'),
    path('about/', views.about , name = 'about'),
    path('contact/', views.contact , name = 'contact'),
    path('services/', views.services , name = 'services'),
    path('signup',views.handleSignup , name = 'handleSignup'),
    path('login',views.handleLogin, name = 'handleLogin'),
    path('logout/',views.handleLogout, name = 'handleLogout'),
   
]
