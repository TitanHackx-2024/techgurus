from enum import Enum
from django.conf import settings
from postify_app.models import Account
from abc import ABC, abstractmethod
from postify_app.services.twitter_utils import upload_to_twitter

class PlatformUploader(ABC):
    @abstractmethod
    def upload(self, content, file_path):
        pass
    
class YoutubeUploader(PlatformUploader):
    def upload(self, content, file_path):
        pass
    
class InstagramUploader(PlatformUploader):
    def upload(self, content, file_path):
        pass

class TwitterUploader(PlatformUploader):
    def upload(self, content, file_path):
        try:
            upload_to_twitter(content, file_path)
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
    
class UploaderService:
    @staticmethod        
    def upload_to_platforms(self, content):
        success_platforms = set()
        failed_platforms = set()
        for platform in content.platforms:
            try:
                UploaderFactory.get_uploader(platform).upload(content, content.file_path)
                success_platforms.add(platform)
            except Exception as e:
                failed_platforms.add(platform)

        return {
            'success_platforms': success_platforms,
            'failed_platforms': failed_platforms
            }