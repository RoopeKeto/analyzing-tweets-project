#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 01:29:12 2019

@author: roope
"""

# creating tesla model 3 data, out of the whole json file

# first importing libraries for handling and plotting dat
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

tweets_data_path = '/home/roope/projects/sentiment_analysis/sentiment analysis advanced/tesla_data.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets_file.close()

# let's see the firts tweet what it looks like
#print(tweets_data[0])

#print("type of the tweets_data: ", type(tweets_data))
# let's print the number of items in the list

#print("number of tweets: ", len(tweets_data)) #16476
# let's print only the text of the tweet of the first tweet

#print("\nText of the first tweet: \n",tweets_data[0]['text']) # nähdään että puhuu teslasta ja edisonista.
 # -> nämä tulee poistaa, että jos on edison tai nikola, samassa tesla twiitissä, niin poista! 
# let's check if the tweet has extended tweet
 
# the'res all kind of info. Let's take only the texts and made them to a list. 
# however there's problem with the tweets "extended". Some tweets don't show up in full. Let's use following function

# This loads the most comprehensive text portion of the tweet  
# Where "data" is an individual tweet, treated as JSON / dict
def getText(data):       
    # Try for extended text of original tweet, if RT'd (streamer)
    try: text = data['retweeted_status']['extended_tweet']['full_text']
    except: 
        # Try for extended text of an original tweet, if RT'd (REST API)
        try: text = data['retweeted_status']['full_text']
        except:
            # Try for extended text of an original tweet (streamer)
            try: text = data['extended_tweet']['full_text']
            except:
                # Try for extended text of an original tweet (REST API)
                try: text = data['full_text']
                except:
                    # Try for basic text of original tweet if RT'd 
                    try: text = data['retweeted_status']['text']
                    except:
                        # Try for basic text of an original tweet
                        try: text = data['text']
                        except: 
                            # Nothing left to check for
                            text = ''
    return text

# let's use the above function to get the text to an empty list
tweets_text = []
for i in range(len(tweets_data)):
    tweets_text.append(getText(tweets_data[i]))
    

# GETTING retweet status
    

# let's look at the first 100 (using for loop for easier reading)
for i in range(2):
    print(i, " ", tweets_text[i], "\n")    
    

    
    
# we can see that some tweets are not about tesla (or the auto models)
# to make sure the tweet is about Tesla, let's zoom in to tweets that contain both Tesla and model 3

# loop
model3_tweets = []

for i in range(len(tweets_text)):
    if ("tesla" in tweets_text[i].lower() and ("model 3" in tweets_text[i].lower())):
        model3_tweets.append(tweets_text[i])

# let's print out the first twenty out of the model3_tweets: 
print("model 3 tweets first twenty: \n\n")
print(model3_tweets[0:20])
# let's check how many tweets there are about both the tesla and model 3
print(len(model3_tweets)) # so there's 992 tweets. 

# let's do sentiment analysis of these 992 tweets using TextBlob
from textblob import TextBlob

# let's test textblob. with tweet number 19 in the model3_tweets (which looks like an positive one)
# "'@cmaligecyeg @PluginAlberta I have the Tesla Model 3. Works wonderful in Edmonton this winter. I’d be happy to show you it. Just PM me.'"

# first we need to make a textblob out of the string
tweet19 = TextBlob(model3_tweets[19])
# let's use TextBlob's sentiment to check the polarity and subjectivity
print(tweet19.sentiment) # so this got almost as positive polarity as possible (1) and subjectivity 1, seems to be working!

# from source code of textblob we can see, that textblob handles "not great_" as negative poaliryt of -0.4 let's test!
print("not great's sentiment scores: ", TextBlob("not great").sentiment)

# textblob does not use machine learning, but hardcoded rules (that however may work quite well, let's see)

# let's create listing of textblobs out of model 3 tweets and listing of the sentiments ('lets put these into same list)
model3_tweetblobs = []
model3_tweetsentiments = []
# 
for i in range(len(model3_tweets)):
    # get the tweetblob
    model3_tweetblobs.append(TextBlob(model3_tweets[i]))
    # get the sentiment
    sentiment = model3_tweetblobs[i].sentiment
    # let's create list of lists (also including the tweet and the sentiment to ease the association)
    model3_tweetsentiments.append([model3_tweets[i], sentiment])

    
#let's print first 100 of sentiments: 
for i in range(100):
    print("\n", model3_tweetsentiments[i])
    
# let's create  list of just the polarities to see the distribution 
    
model3_tweet_polarities = []
for i in range(len(model3_tweets)):
    model3_tweet_polarities.append(model3_tweetsentiments[i][1].polarity)

# let's see how negative / positive the sentiments are: 
# with 20 bins
plt.hist(plt.hist(model3_tweet_polarities, bins = 30))

# from the plot we can see that there seems to be only handful of very positive and very negative, let's look
# at the negatives first

#let's define function for printing out different sentiments 

def printSentimentsBetweenPolarities(polarity_start, polarity_end, numberof=len(model3_tweetsentiments)):
    sentiments = []
    for i in range(len(model3_tweetsentiments)):
        if (i == numberof):
            return sentiments
        
        if (model3_tweetsentiments[i][1].polarity <= polarity_end) and (model3_tweetsentiments[i][1].polarity >= polarity_start):  
            sentiments.append(model3_tweetsentiments[i])
            print(model3_tweetsentiments[i])
    return sentiments

# using the function for negatives between -1 and -0.2 (inclusive)

# we can see that these are not actually negative ( except for the first one)
negatives = printSentimentsBetweenPolarities(-1, -0.3)

# # TAKING OUT RETWEETS # #
# If we would want to found out some user generated tweets about model 3 (like tweets how bad/good the model 3 is, we would be good to take out retweeted tweets)


# # # # CREATING DATAFRAME # # # #

"""
Let's use tweets_data (contains 291 668 tweets) and... "
Let's make this so, that it only contains model 3 related tweets.
"""

model3_twiitit = []
for i in range(len(tweets_data)):
    teksti = getText(tweets_data[i])
    if ("tesla" in teksti.lower() and ("model 3" in teksti.lower())):
        model3_twiitit.append(tweets_data[i])


def tweets_to_data_frame(tweets):
    df = pd.DataFrame(data=[getText(tweet) for tweet in tweets], columns=['tweets'])
    
    df['id'] = np.array([tweet['id'] for tweet in tweets])
    df['len'] = np.array([len(getText(tweet)) for tweet in tweets])
    df['date'] = np.array([tweet['created_at'] for tweet in tweets])
    df['source'] = np.array([tweet['source'] for tweet in tweets])
    df['likes'] = np.array([tweet['favorite_count'] for tweet in tweets])
    df['retweets'] = np.array([tweet['retweet_count'] for tweet in tweets])
    df['retweeted'] = np.array([('retweeted_status' in tweet)  for  tweet in tweets])
    df['polarity'] = np.array([TextBlob(getText(tweet)).sentiment.polarity for tweet in tweets])
    return df


def remove_retweets(dataframe=df):
    mask = df['retweeted']
    df_noretweets = df[mask]
    return df_noretweets

def filter_by_sentiment(minpol, maxpol, df):
    df_filtered = df[df['polarity'] > minpol]
    df_filtered = df_filtered[df_filtered['polarity'] <= maxpol]
    return df_filtered
    

def remove_duplicates(df):
    text_list = []
    polarities = []
    for i, text in enumerate(df['tweets'], 0):
        if (i < 10):
            print(i)
        if text not in text_list:
            text_list.append(text)
            polarities.append(df['polarity'].values[i])
        no_duplicates_list = [text_list, polarities]
    return no_duplicates_list