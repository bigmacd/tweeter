#!/usr/bin/env python3
"""
Twitter/X Tweet Posting Script
Requires Twitter API v2 credentials and tweepy library
"""

import tweepy
from tweepy.errors import Forbidden, BadRequest, NotFound, Unauthorized

import os
from typing import Optional

class TwitterPoster:
    def __init__(self):
        """Initialize Twitter API client with credentials from environment variables"""
        # Twitter API credentials (set these as environment variables)
        api_key = os.getenv('apiKey')
        api_secret = os.getenv('apiKeySecret')
        access_token = os.getenv('accessToken')
        access_token_secret = os.getenv('accessTokenSecret')
        bearer_token = os.getenv('bearerToken')
        
        if not all([api_key, api_secret, access_token, access_token_secret]):
            raise ValueError("Missing required Twitter API credentials in environment variables")
        
        # Initialize the Twitter API v2 client
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
    
    def post_tweet(self, text: str, reply_to_id: Optional[str] = None) -> dict:
        """
        Post a tweet to Twitter/X
        
        Args:
            text (str): The tweet text (max 280 characters)
            reply_to_id (str, optional): Tweet ID to reply to
            
        Returns:
            dict: Response from Twitter API containing tweet information
        """
        retVal = { 'id': '0' }
        try:
            if len(text) > 280:
                raise ValueError(f"Tweet text is too long: {len(text)} characters (max 280)")
            
            try:
                # Post the tweet
                response = self.client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=reply_to_id
                )
                print(f"✅ Tweet posted successfully!")
                print(f"Tweet ID: {response.data['id']}")
                print(f"Tweet URL: https://twitter.com/user/status/{response.data['id']}")
                retVal['id'] = response.data['id']

            except (Forbidden, BadRequest, NotFound, Unauthorized) as e:
                print(f"caught error posting tweet {str(e)}")
                #raise(ValueError(f"Error posting tweet: {str(e)}"))

            return retVal
            
        except Exception as e:
            print(f"❌ Error posting tweet: {str(e)}")
            raise
    
    def post_thread(self, tweets: list) -> list:
        """
        Post a thread of tweets
        
        Args:
            tweets (list): List of tweet texts
            
        Returns:
            list: List of tweet IDs from the thread
        """
        if not tweets:
            raise ValueError("Tweet list cannot be empty")
        
        tweet_ids = []
        reply_to_id = None
        
        for i, tweet_text in enumerate(tweets):
            print(f"Posting tweet {i+1}/{len(tweets)}...")
            
            response = self.post_tweet(tweet_text, reply_to_id)
            tweet_ids.append(response['id'])
            reply_to_id = response['id']  # Next tweet will reply to this one
        
        print(f"✅ Thread of {len(tweets)} tweets posted successfully!")
        return tweet_ids

def main():
    """Example usage of the TwitterPoster class"""
    try:
        # Initialize the Twitter poster
        poster = TwitterPoster()
        
        # Example 1: Post a single tweet
        single_tweet = "Hello from my Python script! 🐍 #Python #TwitterAPI"
        poster.post_tweet(single_tweet)
        
        # Example 2: Post a thread
        thread_tweets = [
            "🧵 Here's a thread about Python and Twitter API (1/3)",
            "The Twitter API v2 makes it easy to post tweets programmatically using libraries like tweepy (2/3)",
            "You can post single tweets, replies, and even entire threads with just a few lines of code! (3/3)"
        ]
        poster.post_thread(thread_tweets)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have set the following environment variables:")
        print("- TWITTER_API_KEY")
        print("- TWITTER_API_SECRET") 
        print("- TWITTER_ACCESS_TOKEN")
        print("- TWITTER_ACCESS_TOKEN_SECRET")
        print("- TWITTER_BEARER_TOKEN")

if __name__ == "__main__":
    main()
