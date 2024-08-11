from rest_framework import serializers
from core.models import Content, Platform

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']

class ContentSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    editor = serializers.ReadOnlyField(source='editor.username')
    platforms = PlatformSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'text_content', 'content_type', 
                  'created_by', 'editor', 'scheduled_time', 'status', 'platforms', 
                  'raw_content', 'edited_content']
        read_only_fields = ['content_id', 'created_by', 'editor']

class ContentCreateSerializer(serializers.ModelSerializer):
    platforms = serializers.PrimaryKeyRelatedField(queryset=Platform.objects.all(), many=True, required=False)

    class Meta:
        model = Content
        fields = ['title', 'description', 'text_content', 'content_type', 'scheduled_time', 'platforms', 'raw_content']

    def create(self, validated_data):
        platforms = validated_data.pop('platforms', [])
        content = Content.objects.create(**validated_data)
        content.platforms.set(platforms)
        return content