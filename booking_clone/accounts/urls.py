from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('verify-account/<token>/', views.verify_email_token, name="verify_email_token")
]
