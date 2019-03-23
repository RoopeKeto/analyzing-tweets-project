#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 01:26:01 2019

Code based on vprusso's youtube tutorial on twitter scraping

"""

# creating tweepy streamer

# let's import necessary modules
from tweepy import API
from tweepy import cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

class TwitterClient():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
    
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets
class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth =  OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth
    
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #This handles twitter  authentication and the connection to the Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        
        stream = Stream(auth, listener, tweet_mode = 'extended')
        
        # this line filter twitter streams to capture data by the keywords:
        stream.filter(track=hash_tag_list, languages=["en"])
      
class TwitterListener(StreamListener):
    """
    This is a basic listener class that just print received tweets to stdout. 
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        
    def on_data(self, data):
        try:

            with open (self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        
    
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


if __name__ == "__main__":
    
    hash_tag_list = ["tesla", "bmw", "audi", "volkswagen", "jaguar","toyota"]
    fetched_tweets_filename = "autoyhtiot_tweetit.json"
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
