from enum import Enum
from django.conf import settings
from postify_app.models import Content , ContentPlatform
from abc import ABC, abstractmethod
from postify_app.services.twitter_client import upload_to_twitter

class PlatformUploader(ABC):
    @abstractmethod
    def upload(self, content):
        pass
    
class YoutubeUploader(PlatformUploader):
    def upload(self, content):
        pass
    
class InstagramUploader(PlatformUploader):
    def upload(self, content):
        pass

class TwitterUploader(PlatformUploader):
    def upload(self, content):
        try:
            upload_to_twitter(content)
        except Exception as e:
            print("exception: ", e)
    

class UploaderFactory:
    @staticmethod
    def get_uploader(platform):
        if platform == 'youtube':
            return YoutubeUploader()
        elif platform == 'instagram':
            return InstagramUploader()
        elif platform == 'twitter':
            return TwitterUploader()
        else:
            raise ValueError("Invalid platform")
    
class UploaderService:
    @staticmethod        
    def upload_to_platforms(content):
        print("calling here--->", content.platforms)
        success_platforms = set()
        failed_platforms = set()
        for platform in content.platforms.all():
            print("platform",platform)
            try:
                UploaderFactory.get_uploader(platform.ui_mapping_name).upload(content)
                platform_content = ContentPlatform.objects.get(content_id=content, platform_id_id=platform.platform_id)
                platform_content.upload_status = 'success'
                platform_content.save()
                success_platforms.add(platform.ui_mapping_name)
            except Exception as e:
                print("exception at upload: ", e)
                failed_platforms.add(platform)

        return success_platforms , failed_platforms