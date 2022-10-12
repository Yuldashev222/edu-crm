import json

from django.contrib.auth.models import update_last_login
from django.core import exceptions
from django.contrib.auth import password_validation, hashers, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime

from api.v1.general.enums import ProfileRoles
from api.v1.company.serializers.company_serializers import GetCompanySerializers
from . import models, services, enums


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'father_name', 'phone_number', 'role', 'section')


class UserTokenSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserRetrieveSerializer(self.user).data
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class StudentSerializer(serializers.ModelSerializer):
    creator_id = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.Student
        exclude = ('username', 'role', 'section', 'is_staff', 'is_admin', 'is_superuser')

        read_only_fields = ('creator',)

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['role'] = ProfileRoles.student.value

        return super().create(validated_data)

    def update(self, instance, validated_data):

        errors = {}
        company = validated_data.get('company')
        phone_number = validated_data.get('phone_number')

        # checking that the second phone number is not equal to the first phone number -----------
        second_phone_number = validated_data.get('second_phone_number')

        if (
                second_phone_number and second_phone_number == instance.phone_number or
                second_phone_number and phone_number and phone_number == second_phone_number
        ):
            errors['second_phone_number'] = ['the additional phone number is the same as the main phone number']
        # ----------------------------------------------------------------------------------------

        if company and phone_number:
            if company.id != instance.company.id or phone_number != instance.phone_number:

                if not services.username_not_in_database(company_id=company.id, phone_number=phone_number):
                    errors['company'] = ['this phone number is registered with this company']

        elif company:
            if company.id != instance.company_id:

                if not services.username_not_in_database(company_id=company.id, phone_number=instance.phone_number):
                    errors['company'] = ['this phone number is registered with this company']

        elif phone_number:
            if phone_number != instance.phone_number:

                if not services.username_not_in_database(company_id=instance.company_id, phone_number=phone_number):
                    errors['phone_number'] = ['this phone number is registered in the company']

        if errors:
            raise serializers.ValidationError(errors)

        return super().update(instance, validated_data)

    def validate(self, data):
        user = models.Student(**data)

        errors = dict()

        # date_start and date_finished validations  ----------------------
        date_start = data.get('date_start')
        date_finished = data.get('date_finished')
        today_date = datetime.today().date()

        if date_start and date_finished:

            if date_start < today_date:
                errors['date_start'] = ['start date before today\'s date.']

            if date_start >= date_finished:
                errors['date_finished'] = ['end date before start date.']

        elif date_start:

            if date_start < today_date:
                errors['date_start'] = ['start date before today\'s date.']

        elif date_finished:
            data['date_start'] = today_date
            if date_finished <= today_date:
                errors['date_finished'] = ['end date before today\'s date']
        # --------------------------------------------------------------------

        # password validations -----------------------------------------------
        password = data.get('password')
        if password:
            try:
                password_validation.validate_password(password=password, user=user)

            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)

            data['password'] = hashers.make_password(data['password'])
        # --------------------------------------------------------------------

        if errors:
            raise serializers.ValidationError(errors)

        return super(StudentSerializer, self).validate(data)
