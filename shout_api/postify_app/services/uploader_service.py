from enum import Enum
from django.conf import settings
from postify_app.models import Account
from abc import ABC, abstractmethod
from postify_app.services.twitter_utils import upload_to_twitter
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials


class PlatformUploader(ABC):
    
    @abstractmethod
    def upload(self, content, file_path):
        pass
    
class YoutubeUploader(PlatformUploader):
    def __init__(self):
        self.client = None

    def authenticate(self, credentials_json):
        credentials = Credentials.from_authorized_user_file(credentials_json)
        self.client = build('youtube', 'v3', credentials=credentials)

    def upload(self, content, file_path):
        try:
            if not self.client:
                raise Exception("YouTube client not authenticated")

            media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
            request = self.client.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": content.title,
                        "description": content.description,
                    },
                    "status": {
                        "privacyStatus": "private"  # Change if needed
                    }
                },
                media_body=media
            )

            response = request.execute()
            content_id = response.get('id')
            return content_id
        except Exception as err:
            print("exception: ", err)


class InstagramUploader(PlatformUploader):
    def upload(self, content, file_path):
        try:
            upload_to_twitter(content, file_path)
        except Exception as e:
            print("exception: ", e)
    
class TwitterUploader(PlatformUploader):
    def upload(self, content, file_path):
        pass

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
    def upload_to_platforms(self, content, credentials_json_path=None):
        success_platforms = set()
        failed_platforms = set()
        for platform in content.platforms:
            try:
                uploader = UploaderFactory.get_uploader(platform)
                if isinstance(uploader, YoutubeUploader):
                    
                    uploader.authenticate(credentials_json_path)
                uploader.upload(content, content.file_path)
                success_platforms.add(platform)
            except Exception as e:
                print(f"Failed to upload to {platform.value}: {e}")
                failed_platforms.add(platform)
        return {
            'success_platforms': success_platforms,
            'failed_platforms': failed_platforms
            }