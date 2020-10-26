from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "dashboard"
urlpatterns = [
    path('otp/<str:email2>', views.otp_verify, name="otp_verify"),
    path('dashboard', views.dashboard, name="dashboard"),
    path("users", views.UserListView.as_view(), name="users"),
    path('profile/follow/<int:pk>', views.follow, name="follow"),
    path('profile/unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('profile/<pk>', views.ProfileDetailView, name="profile"),
    path('editprofilepic', views.EditProfilePic, name="editprofilepic"),
    path('editprofile', views.EditProfile, name="editprofile"),
    path('change_password', views.change_password, name='change_password'),
    path('security', views.security, name="security"),
    path('EmailUpdate', views.EmailUpdate, name="EmailUpdate"),
    path('email_activated', views.email_activated, name="email_activated"),
    path('email_activated_false', views.email_activated_false, name="email_activated_false"),
    path('PhoneUpdate', views.PhoneUpdate, name="PhoneUpdate"),
    path('otp_phone_veify/<str:phone>', views.otp_phone_verify, name="otp_phone_verify"),
    path('delete/profile/<int:pk>', views.DeleteUser.as_view(), name="delete"),
    path('notify/', views.notify, name="notify"),
    path('billing', views.billing, name="billing"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
