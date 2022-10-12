from django.urls import path, re_path, include


from . import routers as account_routers
from .views import token_views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from .views.account_views import TestView

urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('', include(account_routers.USER_CRUD_ROUTER.urls)),

    path('login/', token_views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

]
