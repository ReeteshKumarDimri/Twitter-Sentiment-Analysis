from flask import Flask, render_template, request, redirect, url_for
from numpy import negative
from config import *
import tweepy
from textblob import TextBlob
import wget

#instantiating the api
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
#creating api object
api = tweepy.API(auth,wait_on_rate_limit=True)

TotalTweets = 0
positiveTweets = 0
negativeTweets = 0
neutralTweets = 0

def Analysis(key):
    global positiveTweets
    global neutralTweets
    global negativeTweets
    global TotalTweets
    for tweet in tweepy.Cursor(api.search_tweets, q=key).items(300):
        finaltext = tweet.text.replace('RT','')
        if finaltext.startswith(' @'):
            pos = finaltext.index(':')
            finaltext = finaltext[pos+2:]
        if finaltext.startswith('@'):
            pos = finaltext.index(' ')
            finaltext = finaltext[pos+2:]
        analysis = TextBlob(finaltext)
        tweetPolarity = analysis.polarity

        if tweetPolarity < 0.00:
            negativeTweets+=1
        elif tweetPolarity > 0.00:
            positiveTweets+=1
        elif tweetPolarity == 0.00:
            neutralTweets+=1
        
        TotalTweets+=1



#Creating flask object
app=Flask(__name__)

#First Page.
@app.route("/")
def home_page():
    return render_template("form.html")

@app.route("/Fetch_Data",methods=['POST','GET'])

def Fetch_Data():
    if request.method=="POST":
        key=request.form["q"]
        if key == "":
            return render_template("form.html",warning="Please enter a keyword !",c = 'warn')
        Analysis(key)
        positive = round(positiveTweets/TotalTweets*100,2) 
        negative = round(negativeTweets/TotalTweets*100,2) 
        neutral = round(neutralTweets/TotalTweets*100,2) 
        return render_template("form.html",
        pos = positive,
        neg = negative,
        neu = neutral,
        disp = True,c = 'INFO',warning = "Analysis for the keyword : "+key)



if __name__ =="__main__":
    app.run(debug= True)

            