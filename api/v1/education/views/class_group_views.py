from django.shortcuts import render
from api.v1.general.service import create_data
from rest_framework import permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from api.v1.education.models.class_group import (
    Rooms,
)

from api.v1.education.serializers.class_group_serializer import (
    CretaRoomsSerializers,
)

class RoomsListCreateViews(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(request_body=CretaRoomsSerializers)
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        data = create_data(CretaRoomsSerializers(data=request.data))
        if data.get('success') == True:
            return Response(
                data, status=status.HTTP_201_CREATED
            )
        return Response(
                data, status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request, format=None):
        data = create_data(CretaRoomsSerializers(data=request.data))
        if data.get('success') == True:
            return Response(
                data, status=status.HTTP_201_CREATED
            )
        return Response(
                data, status=status.HTTP_400_BAD_REQUEST
            )

