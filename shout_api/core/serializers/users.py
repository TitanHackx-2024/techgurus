from rest_framework import serializers
from core.models import User, Account, Role

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    account_name = serializers.CharField(write_only=True, required=False)
    is_editor = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'account_name', 'is_editor')

    def create(self, validated_data):
        account_name = validated_data.pop('account_name', None)
        if account_name:
            account = Account.objects.get(account_name=account_name)
        else:
            account = None
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_editor=validated_data.get('is_editor', False),
            account=account
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'account', 'is_editor')
        read_only_fields = ('account',)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'