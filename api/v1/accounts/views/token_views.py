from rest_framework import (
    response, 
    status, 
    serializers as rest_serializers
)
from rest_framework_simplejwt import (
    views as jwt_views, 
    exceptions as jwt_exceptions, 
)

from api.v1.company.models.models import Company
from .. import serializers


class UserTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.UserTokenSerializer
    
    def post(self, request, *args, **kwargs):

        domain_name, phone_number, password = (
            request.data.get('domain_name'),
            request.data.get('phone_number'),
            request.data.get('password')
        )
        errors = dict()

        if not domain_name:
            errors['domain_name'] = ['This field is required.']
        else:
            try:
                company_id = Company.objects.get(domain_name=domain_name).id
            except Company.DoesNotExist:
                errors['domain_name'] = ['This domain name does not exist.']

        if not phone_number:
            errors['phone_number'] = ['This field is required.']

        if not password:
            errors['password'] = ['This field is required.']

        if errors:
            raise rest_serializers.ValidationError(errors)

        data = request.data.copy()
        data['username'] = str(company_id) + '|' + str(phone_number)
        del data['phone_number'], data['domain_name']

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exceptions.TokenError as e:
            raise jwt_exceptions.InvalidToken(e.args[0])

        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)
