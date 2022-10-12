from django.urls import path

from api.v1.company.views.company_view import (
    CreateCompanyView,
    GetUpdateDeleteCompanyView,
)


urlpatterns = [
    path('create/', CreateCompanyView.as_view()),
    path('detail/<int:pk>/', GetUpdateDeleteCompanyView.as_view()),
]
