from rest_framework import routers

from . import models

from .views import account_views


USER_CRUD_ROUTER = routers.SimpleRouter()

USER_CRUD_ROUTER.register('students', account_views.StudentAPIViewSet, basename='students')












