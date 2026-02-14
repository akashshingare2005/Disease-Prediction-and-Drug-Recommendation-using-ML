from django.urls import path
from .views import predict, register, login_user, get_history, generate_report

urlpatterns = [
    path("predict/", predict),
    path("register/", register),
    path("login/", login_user),
    path("history/", get_history),
    path("report/", generate_report),
]
