from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Account, Content , User , Platform, ContentPlatform


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
# class ContentPlatformSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContentPlatform
#         fields = '__all__'
        
class ContentSerializer(serializers.ModelSerializer):
    platforms = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Content
        fields = '__all__'

    def create(self, validated_data):
        platforms = validated_data.pop('platforms', [])
        instance = super().create(validated_data)
        for platform_id in platforms:
            ContentPlatform.objects.create(content_id=instance, platform_id_id=platform_id)
        return instance

    def update(self, instance, validated_data):
        platforms = validated_data.pop('platforms', [])
        instance = super().update(instance, validated_data)
        ContentPlatform.objects.filter(content_id=instance).delete()
        for platform_id in platforms:
            ContentPlatform.objects.create(content_id=instance, platform_id_id=platform_id)
        
        return instance   

    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['platforms'] = instance.platforms.values_list('platform_id', flat=True)
        return response    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(required=True)
    account_id = serializers.IntegerField(required=True)

    def validate(self, data):
        account_id = data.get('account_id')
        email = data.get('email')
        password = data.get('password')

        try:
            account = Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            raise serializers.ValidationError("account_id does not exist")

        user = account.user_set.filter(email_address=email).first()
        if user is None:
            raise serializers.ValidationError("User does not exist.")
        
        if user.password_hash != password:
            raise serializers.ValidationError("Invalid password")

        print(type(user), )
        return {'user': user}


class TokenSerializer(serializers.Serializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    def create(self, validated_data):
        pass

    @staticmethod
    def get_access_token(user):
        try:

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            print(f'Access token generated for user {user.phone_number}.')
            return access_token
        except Exception as e:
            print(f'Error generating access token for user {user.phone_number}: {str(e)}')
            return None

    @staticmethod
    def get_refresh_token(user):
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            print(f'Refresh token generated for user {user.phone_number}.')
            return refresh_token
        except Exception as e:
            print(f'Error generating refresh token for user {user.phone_number}: {str(e)}')
            return None

    def update(self, instance, validated_data):
        pass


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User
