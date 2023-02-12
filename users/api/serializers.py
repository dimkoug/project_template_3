from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','email', 'first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id','username','password','email', 'first_name', 'last_name', 'token')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)




class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
