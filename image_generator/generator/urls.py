from . import views
from django.urls import path

urlpatterns = [
    path("",views.home,name = "home"),
    path("generator",views.generator , name = "generator"),
    path("register", views.register, name = "register"),
    path("login", views.login, name = "login"),
    path("logout", views.logout, name = "logout"),
    path("feedback", views.feedback, name = "feedback"),
]