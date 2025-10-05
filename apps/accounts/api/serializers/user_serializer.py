from rest_framework import serializers
from apps.accounts.models import User
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")
        
class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'document_type',
            'document_id',
            'phone_number',
            'country',
            'city',
            'address',
            'is_active',
            'is_staff',
            'last_login',
            'groups'
        ]