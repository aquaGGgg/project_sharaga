from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_framework import routers

from game_site_api.views import UserViewSet, ProfilePicViewSet, PostViewSet, PostPicViewSet, PostComentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfilePicViewSet)
router.register(r'posts', PostViewSet)
router.register(r'post-pics', PostPicViewSet)
router.register(r'post-coment', PostComentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]