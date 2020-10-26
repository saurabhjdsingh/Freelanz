from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('confirm_your_account', views.confirm_your_account, name="confirm_your_account"),
    path('account_activated', views.account_activated, name="account_activated"),
    path('account_activated_false', views.account_activated_false, name="account_activated_false"),
 
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
