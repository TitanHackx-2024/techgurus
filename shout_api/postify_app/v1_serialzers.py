from rest_framework import serializers
from .models import Account, Content , User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    