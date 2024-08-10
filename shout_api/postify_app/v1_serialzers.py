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
        # exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        platforms = validated_data.pop('platforms', [])
        content = Content.objects.create(**validated_data)
        # Create ContentPlatform entries
        for platform_id in platforms:
            ContentPlatform.objects.create(content_id=content, platform_id_id=platform_id)
        return super().create(validated_data)    
     
    def update(self, instance, validated_data):
        platforms = validated_data.pop('platforms', [])
        instance = super().update(instance, validated_data)
        # Clear existing platforms and add new ones
        ContentPlatform.objects.filter(content_id=instance).delete()
        for platform_id in platforms:
            ContentPlatform.objects.create(content_id=instance, platform_id_id=platform_id)
        
        return instance   
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['platforms'] = instance.platforms.values_list('platform_id', flat=True)
        return response    