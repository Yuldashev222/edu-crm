from pyexpat import model
from rest_framework import serializers

from api.v1.education.models.class_group import (
    Rooms,
)

class CretaRoomsSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    number_room = serializers.CharField(required=True)
    class Meta:
        model = Rooms
        fields = ('name', 'number_room')
        
    # def save(self, validated_data):
    #     pass