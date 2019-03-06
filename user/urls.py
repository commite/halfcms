from django.urls import path, include, re_path
from base import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user/new', views.sign_up, name="sign_up"),
    path('user/login', views.sign_in, name="sign_in"),
    path('user/logout', views.logout_user, name="logout_user"),
    path('user/user-page', views.user_page, name="user_page"),
    path('user/magic-link', views.create_magic_link, name="magic_link"),
    re_path('user/magic-confirm/(?P<activation_key>\w+)/',
            views.magic_login_confirm, name="magic_confirm"),
    path('registration/', include('django.contrib.auth.urls'))
]
