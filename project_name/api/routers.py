from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views as api_views
from rest_framework_simplejwt import views as jwt_views

from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'groups', viewsets.GroupViewSet)

urlpatterns = router.urls + [
    path('current_user/', viewsets.current_user),
    path('register/', viewsets.RegisterApi.as_view()),
    path('api-token-auth/', api_views.obtain_auth_token, name='api-token'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
          name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
    #      name='token_refresh'),
    # path('users/', UserList.as_view())
]