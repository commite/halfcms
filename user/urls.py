from django.urls import path
from base import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/new', views.sign_up, name='sign_up'),
    ]
