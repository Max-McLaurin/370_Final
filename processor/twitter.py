import tweepy

# Credentials (assuming these are imported or defined within this script)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHhdtgEAAAAAzyTI61RTi9eyvWpMkaEsHbVlaZs%3DDf18EVNElHJZJp1O4zdIag1eGK4j1HrjpKoDztUrPtWnfMJQgy'
consumer_key = 'yM4eMeEz6st75EjJrjxoCsn4q'
consumer_secret = '9fAme6T55FTVMo9iCkduMcjcvUC4irssgsF4rQUfyINLK0xrof'
access_token = '1038707698718699520-nnPdMS4HOZQjuYTl1NdGpbBEGJoLuH'
access_token_secret = 'p6P2qvMvLg7IQFPMUAS4ECR9QDDE7JAexpi4D35IC38pC'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True
)

def load_image(img_path):
    media_id = api.media_upload(filename = img_path).media_id_string
    return media_id

def tweet_text(text):
    client.create_tweet(text = text)
    print("Tweeted: " + text)

def tweet_text_and_media(text, media):
    media_id = load_image(media)
    client.create_tweet(text = text, media_ids = [media_id])
    print(f"\n\tTwitter Bot: Successfully Tweeted!\n\n{text}\n\nMedia ID:  {media_id}\n\n")


tweet_text_and_media("Daily Weather: ", "weather_dashboard.png")

