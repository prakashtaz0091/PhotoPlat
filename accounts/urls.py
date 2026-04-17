from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register_page"),
    path("login/", views.login_view, name="login_page"),
    path("logout/", views.logout_view, name="logout_page"),
    path("profile/", views.profile_view, name="profile_page"),
    path("submit-kyc/", views.submit_kyc, name="submit_kyc_page"),
    path("profile-photo/upload/", views.upload_profile_photo, name="upload_profile_photo_page"),
    path("profile-photo/delete/", views.remove_profile_photo, name="remove_profile_photo_page"),
]