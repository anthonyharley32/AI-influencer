import openai
import tweepy
from dotenv import load_dotenv
import os

load_dotenv('../keys.env')

# OpenAI API setup
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Twitter API setup
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Test the authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print(f"Authentication failed: {e}")

# Update Twitter API setup
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def generate_post(prompt):
    openai_client = openai.OpenAI(api_key=openai.api_key)  # Renamed client to openai_client
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate model, e.g., "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def post_to_twitter(content):
    try:
        response = client.create_tweet(text=content)  # Unchanged
        print(f"Tweet posted successfully. Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"An error occurred while posting the tweet: {e}")

if __name__ == "__main__":
    prompt = "Write a quote from a business leader."
    post_content = generate_post(prompt)
    post_to_twitter(post_content)
    print(f"Posted to Twitter: {post_content}")