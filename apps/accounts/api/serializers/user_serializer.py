from rest_framework import serializers
from apps.accounts.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

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
            'first_name',
            'last_name',
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
        
class UserUpdateSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), write_only=True, source='groups'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'groups',
            'group_ids'
        ]

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        instance = super().update(instance, validated_data)
        if groups is not None:
            instance.groups.set(groups)
        return instance
    
class UserUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active',
        ]

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        instance = super().update(instance, validated_data)
        if groups is not None:
            instance.groups.set(groups)
        return instance   
      
class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','password','groups')
        
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("The password must have more than 8 characters.")
        if data.lower() == data:
            raise ValidationError("The password must have at least one capital letter.")
        return data
    
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        user = User.objects.create_user(**validated_data)
        if groups_data:
            group_ids = [group.id for group in groups_data]
            groups = Group.objects.filter(id__in=group_ids)
            user.groups.set(groups)
        user.save()
    
        return user