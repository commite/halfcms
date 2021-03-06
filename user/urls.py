from django.urls import path, include
from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/new', views.sign_up, name='sign_up'),
    path('user/login', views.sign_in, name="sign_in"),
    path('user/logout', views.logout_user, name="logout_user"),
    path('user/user-page', views.user_page, name="user_page"),
    path('registration/', include('django.contrib.auth.urls')),
]
