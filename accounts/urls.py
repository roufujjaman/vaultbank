from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.AccountView.as_view(), name="home"),
    path("create", views.create_account, name="create"),
    path("login", views.login_account, name="login"),
    path("logout", views.logout_account, name="logout"),
    path("<int:id>", views.edit_account, name=""),
]