from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orders", views.orders, name="orders"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("singup", views.singup, name="singup"),
    path("yourOrder", views.yourOrder, name="yourOrder")
]
