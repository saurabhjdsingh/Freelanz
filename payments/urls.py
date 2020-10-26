from django.urls import path
from . import views


app_name = "payments"

urlpatterns = [
    path('<str:slug>/<str:name>', views.confirm_payment, name="confirm_payment"),
    path('confirmpayment/', views.payment_status, name="confirmpayment"),
    path('processpayment/', views.processwithdrawal, name="processpayment")
]
