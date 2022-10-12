import json
from rest_framework import (
    viewsets,
    generics,
    response,
    status,
    permissions,
    mixins,
    views,
    serializers as rest_serializers,
)

from api.v1.general.enums import Sections, ProfileRoles
from .. import (
    models,
    serializers,
    permissions as account_permissions,
    services,
    enums,
)
from api.v1.company.models.models import Company


# class UserRetrieveAPIView(generics.RetrieveAPIView):
#
#     serializer_class = serializers.UserRetrieveSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class TestView(views.APIView):

    def post(self, request, *args, **kwargs):
        return response.Response({'d1': 1, 'd2': 11}, status.HTTP_409_CONFLICT)


class StudentAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    permission_classes = (account_permissions.IsOwnerOrReadOnly,)

    # parser_classes = (parsers.MultiPartParser, )

    def get_queryset(self):

        students = models.Student.objects.exclude(
            role=ProfileRoles.developer.value
            # is_deleted=False,
            # is_active=True,
            # date_start__lte=datetime.today().date(),
            # date_finished__gt=datetime.today().date()
        ).order_by('-date_joined')
        return students

    def create(self, request, *args, **kwargs):
        company_id, phone_number = self.request.user.company_id, request.data.get('phone_number')

        if services.username_not_in_database(company_id, phone_number):
            data = request.data.copy()

            username = str(company_id) + '|' + str(phone_number)

            data['username'] = username
            data['section'] = Sections.education.value

            if not data.get('is_active'):
                data['is_active'] = 'true'

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            print(serializer)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            company = Company.objects.get(id=int(company_id))
            errors = {
                'phone_number': 'this << {} >> phone number is registered from the << {} >> company.'.format(
                    phone_number, company.name.title())
            }
            return response.Response(data=errors, status=status.HTTP_409_CONFLICT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
