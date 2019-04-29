from .views import LoginUser, logoutuser, CreateLocker, view_locker
from django.urls import path
from django.contrib.auth.decorators import login_required as lr
urlpatterns = [
    path('', LoginUser.as_view(), name="login_page"),
    path('logout/', logoutuser, name="logout_page"),
    path('create/', CreateLocker.as_view(), name="create_page"),
    path('list/', view_locker, name="list_page"),
]
