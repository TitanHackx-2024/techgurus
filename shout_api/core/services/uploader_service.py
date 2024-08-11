from enum import Enum
from django.conf import settings
from core.models import Content , ContentPlatform
from abc import ABC, abstractmethod
from core.services.twitter_client import upload_to_twitter
from core.services.youtube_client import YoutubeClient

class PlatformUploader(ABC):
    @abstractmethod
    def upload(self, content):
        pass
    
class YoutubeUploader(PlatformUploader):
    def upload(self, content):
        try:
            YoutubeClient().upload(content)
        except Exception as e:
            print("exception: ", e)
    
class InstagramUploader(PlatformUploader):
    def upload(self, content):
        pass

class TwitterUploader(PlatformUploader):
    def upload(self, content):
        pass
        # try:
        #     upload_to_twitter(content)
        # except Exception as e:
        #     print("exception: ", e)
    

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
        success_platforms = set()
        failed_platforms = set()
        for platform in content.platforms.all():
            try:
                UploaderFactory.get_uploader(platform.name).upload(content)
                platform_content = ContentPlatform.objects.get(content_id=content, platform_id=platform.id)
                platform_content.upload_status = 'success'
                platform_content.save()
                success_platforms.add(platform.name)
            except Exception as e:
                print("exception at upload: ", e)
                failed_platforms.add(platform)

        return success_platforms , failed_platforms
