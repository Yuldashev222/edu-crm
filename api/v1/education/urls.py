from django.urls import path

from api.v1.education.views.class_group_views import (
    RoomsListCreateViews
)


urlpatterns = [
    path('room/create/', RoomsListCreateViews.as_view()),
    # path('detail/<int:pk>/', GetUpdateDeleteCompanyView.as_view()),
]
