from .views import LoginUser, logoutuser, CreateLocker, view_locker, delete_locker
from django.urls import path
urlpatterns = [
    path('', LoginUser.as_view(), name="login_page"),
    path('logout/', logoutuser, name="logout_page"),
    path('create/', CreateLocker.as_view(), name="create_page"),
    path('list/', view_locker, name="list_page"),
    # path('delete/<int:pk>/', DeleteLocker.as_view(), name="delete_page"),
    path('delete/', delete_locker, name="delete_page"),
]
