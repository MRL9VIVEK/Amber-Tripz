from django.contrib import admin
from django.urls import path, include
from account import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register', views.REGISTER, name= "register"),
    path('dologin', views.DO_LOGIN, name= "dologin"),
    path('profile', views.PROFILE, name= "profile"),
    path('name', views.name, name= "name"),
    
    path('profile/update', views.PROFILE_UPDATE, name= "profile_update"),
]