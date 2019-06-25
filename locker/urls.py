from .views import LoginUser, logoutuser, CreateLocker, view_locker, DeleteLocker, UserViewSet
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', LoginUser.as_view(), name="login_page"),
    path('logout/', logoutuser, name="logout_page"),
    path('create/', CreateLocker.as_view(), name="create_page"),
    path('list/', view_locker, name="list_page"),
    path('delete/', DeleteLocker.as_view(), name = "delete_page"),
    path('router', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = "rest_framework")),
]
