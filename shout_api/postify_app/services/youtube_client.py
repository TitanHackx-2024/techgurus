from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

class YoutubeUploader:
    def __init__(self):
        # OAuth 2.0 client secrets file
        # D:\titanhack\techgurus\shout_api\postify_app\services\youtube_cred.json
        self.client_secrets_file = "D:\\titanhack\\techgurus\\shout_api\\postify_app\\services\\youtube_cred.json"
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        # Authenticate and build service
        self.youtube = self.authenticate_youtube()

    def authenticate_youtube(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
        # credentials = flow.run_console()
        credentials = flow.run_local_server(port=0)
        return build('youtube', 'v3', credentials=credentials)

    def upload(self, content):
        try:
            media = self.youtube.videos().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': "Uploaded with Postify",
                        'description': "Uploaded with Postify",
                        'categoryId': '22',
                    },
                    'status': {
                        'privacyStatus': 'private'
                    }
                },
                media_body=MediaFileUpload(content)
            )

            response = media.execute()
            print("response: ", response)
            return response

        except Exception as e:
            print("exception: ", e)
            return False

# Initialize the uploader
ytb = YoutubeUploader()

# Path to your video file
file_path = "D:\\titanhack\\techgurus\\shout_api\\media\\uploads\\Vizhi Moodi.mp4"

# Upload the video
print(ytb.upload(file_path))
