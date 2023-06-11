from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgotpassword'),
    path('password_reset_link/<str:token>', views.password_reset_link, name='password_reset_link'),
    
]