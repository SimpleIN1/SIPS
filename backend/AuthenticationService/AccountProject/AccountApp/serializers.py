from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

UserModel = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ["last_name", "first_name", "middle_name", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data['password']
        del validated_data['password']

        user = UserModel(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()

        return user

    def validate(self, data):

        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data
