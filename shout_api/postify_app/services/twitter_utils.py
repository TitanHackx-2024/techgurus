import tweepy

API_KEY = 'XXXX'
API_SECRET_KEY = 'XXXX'
ACCESS_TOKEN = 'XXXX-XXXX'
ACCESS_TOKEN_SECRET = 'XXXX'

CLIENT_SECRET = "XXXX-XXXX"
CLIENT_ID = "XXXX"
BEARER_TOKEN = "XXXXXXXXXXX"

def upload_to_twitter(tweet_text, media_path,content_id):
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        newapi = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET_KEY,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        media = api.media_upload(media_path)
        newapi.create_tweet(text=tweet_text, media_ids=[media.media_id])
    except Exception as e:
        print("exception: ", e)
        return False
    return True

# D:\titanhack\techgurus\shout_api\postify_app\services\Antoine_Griezmann_Haircut_1_grande.jpg
# text = "YO GRIEZMANNNN GOALZOOO"
# file_path = "D:\\titanhack\\techgurus\\shout_api\\postify_app\\services\\Antoine_Griezmann_Haircut_1_grande.jpg"
# upload_to_twitter(text,file_path,1)


        
        
