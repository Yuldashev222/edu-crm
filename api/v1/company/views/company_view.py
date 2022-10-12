from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status


from api.v1.general.service import (
    create_data,
    delete_data,
    get_data,
    get_object,
    not_found_error,
    update_data
)
from api.v1.company.models.models import (
    Company,
)
from api.v1.company.serializers.company_serializers import (
    CreateCompanySerializers,
    DeleteCompanySerializers,
    GetCompanySerializers,
    UpdateCompanySerializers,
)

# Create your views here.


class CreateCompanyView(APIView):
    @swagger_auto_schema(request_body=CreateCompanySerializers)
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        data = create_data(CreateCompanySerializers(data=request.data))
        if data.get('success') == True:
            return Response(
                data, status=status.HTTP_201_CREATED
            )
        return Response(
                data, status=status.HTTP_400_BAD_REQUEST
            )
        

class GetUpdateDeleteCompanyView(APIView):
    def get_queryset(self):
        items = Company.objects.select_related('in_branch',)
        return items
    
    @action(detail=False, methods=['get'])
    def get(self, request, pk, format=None):
        item = get_object(self.get_queryset(), pk)
        if item:
            serializers = GetCompanySerializers(item)
            return Response(
                get_data(serializers),
                status=status.HTTP_200_OK
            )
        return Response(
            not_found_error(pk),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['patch'])
    @swagger_auto_schema(request_body=UpdateCompanySerializers)
    def patch(self, request, pk, format=None):
        item = get_object(self.get_queryset(), pk)
        if item:
            serializers = UpdateCompanySerializers(item, data=request.data, partial=True)
            return Response(
                update_data(serializers),
                status=status.HTTP_200_OK
            )
        return Response(
            not_found_error(pk),
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def delete(self, request, pk, format=None):
        item = get_object(self.get_queryset(), pk)
        if item:
            data = delete_data(item)
            if data.get('success'):
                return Response(
                    delete_data(item),
                    status=status.HTTP_200_OK
                )
            return Response(
                delete_data(item),
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            not_found_error(pk),
            status=status.HTTP_400_BAD_REQUEST
        )
