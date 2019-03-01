from django.conf.urls import url
from userapp import views

app_name = "userapp"

urlpatterns = [
    url(r'^registration/$', views.register, name="register"),
    url(r"^login/$", views.user_login, name="login"),
]