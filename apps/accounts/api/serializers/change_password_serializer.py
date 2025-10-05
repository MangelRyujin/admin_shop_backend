from rest_framework import serializers
from django.core.validators import MinLengthValidator

class ChangePasswordSerializer(serializers.Serializer):
    password_1 = serializers.CharField(write_only=True, required=True,validators=[MinLengthValidator(8)])
    password_2 = serializers.CharField(write_only=True, required=True,validators=[MinLengthValidator(8)])

    def validate(self, attrs):        
        if attrs.get('password_1') != attrs.get('password_2'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs