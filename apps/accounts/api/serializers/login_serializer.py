
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.accounts.api.serializers.user_serializer import GroupSerializer

User = get_user_model()
        
class CustomUserDetailsSerializer(UserDetailsSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    
    class Meta(UserDetailsSerializer.Meta):
       model = get_user_model()
       fields = UserDetailsSerializer.Meta.fields + ('first_name','last_name','document_type', 'document_id' ,'phone_number','country','city','address','groups')
       
        
    def validate_username(self,data):
        return data
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar claims personalizados al token
        
        token['email'] = user.email
        
        # Agregar roles del usuario (grupos)
        token['groups'] = list(user.groups.values_list('name', flat=True))
        
        # Agregar otros campos personalizados si existen
        if hasattr(user, 'document_type'):
            token['document_type'] = user.document_type
        if hasattr(user, 'document_id'):
            token['document_id'] = user.document_id
        if hasattr(user, 'phone_number'):
            token['phone_number'] = user.phone_number
            
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Usar tu CustomUserDetailsSerializer para la respuesta
        user_serializer = CustomUserDetailsSerializer(self.user)
        
        # Estructura de respuesta que incluye token y user details
        data.update({
            'user': user_serializer.data
        })
        
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Obtener el usuario del token de acceso original
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        
        try:
            # Decodificar el token de acceso para obtener el user_id
            access_token = AccessToken(attrs['access'])
            user_id = access_token['user_id']
            
            # Obtener el usuario
            user = User.objects.get(id=user_id)
            
            # Serializar los datos del usuario
            user_serializer = CustomUserDetailsSerializer(user)
            data['user'] = user_serializer.data
            
        except (TokenError, User.DoesNotExist, KeyError):
            # Si hay algún error, no incluimos los datos del usuario
            pass
            
        return data


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Obtener el usuario del token
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        
        try:
            # Decodificar el token para obtener el user_id
            access_token = AccessToken(attrs['token'])
            user_id = access_token['user_id']
            
            # Obtener el usuario
            user = User.objects.get(id=user_id)
            
            # Serializar los datos del usuario
            user_serializer = CustomUserDetailsSerializer(user)
            data['user'] = user_serializer.data
            
        except (TokenError, User.DoesNotExist, KeyError):
            # Si hay algún error, no incluimos los datos del usuario
            pass
            
        return data