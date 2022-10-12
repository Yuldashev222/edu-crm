from rest_framework import serializers

from api.v1.company.models.models import (
    Company,
)



class CreateCompanySerializers(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    class Meta:
        model = Company
        fields = ('name', 'email',)

class GetCompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('last_updated', 'is_active', 'is_deleted',)
        

class UpdateCompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('created_at', 'last_updated', 'is_active', 'is_deleted', 'in_branch',)
        

class DeleteCompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('pk', 'is_active', 'is_deleted')