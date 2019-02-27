from django.urls import path
from base import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/new', views.sign_up, name='sign_up'),
    path('user/login', views.sign_in, name="sign_in"),
    path('user/user_page', views.user_page, name="user_page"),
    ]
