from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from django.conf  import settings
import os

class YoutubeClient:
    def __init__(self):
        # OAuth 2.0 client secrets file
        # D:\titanhack\techgurus\shout_api\postify_app\services\youtube_cred.json
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.client_secrets_file = os.path.join(current_folder, 'youtube_creds.json')
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        # Authenticate and build service
        self.youtube = self.authenticate_youtube()

    def authenticate_youtube(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
        # credentials = flow.run_console()
        credentials = flow.run_local_server(port=0)
        return build('youtube', 'v3', credentials=credentials)


    def upload(self, content):        
        if not content.edited_content and content.content_type != 'Video':
            print("No files to upload to youtube")
            return False
        try:
            media = self.youtube.videos().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': content.title,
                        'description': content.description,
                        'categoryId': '24', # entertainment
                    },
                    'status': {
                        'privacyStatus': 'public'
                    }
                },
                media_body=MediaFileUpload(content.edited_content.path)
            )

            response = media.execute()
            print("response from youtube_client: ", response)
            return response

        except Exception as e:
            print("exception at youtube_client: ", e)
            return False
