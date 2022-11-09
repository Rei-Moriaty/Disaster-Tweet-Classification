from flask import Flask, render_template
from flask import request
import pandas as pd
import numpy as np
import pickle
from flask import jsonify
import tweepy

from transformation import transform

app = Flask("tweet_classifier", template_folder='pages')
output_file = './rf_n_estimator=200_depth=15.bin'
configuration_file = './config.txt'


with open(output_file, 'rb') as f_in:
    (threshold, tags_set, vectorizer, model) = pickle.load(f_in)

with open(configuration_file, 'r') as f_in:
    consumer_key = f_in.readline().strip()
    consumer_secret = f_in.readline().strip()
    access_key = f_in.readline().strip()
    access_secret = f_in.readline().strip()

@app.route('/', methods = ['GET'])
def home():
    tweets = get_tweets()
    disaster_tweets = list()
    non_disaster_tweets = list()
    for tweet in tweets:
        var_class = predict({"text" : tweet.text})
        if var_class == 1:
            disaster_tweets.append(tweet)
        else:
            non_disaster_tweets.append(tweet)
    return render_template('home.html', 
                            disaster_tweets =  disaster_tweets, 
                            non_disaster_tweets =  non_disaster_tweets,
                            len_disaster = len(disaster_tweets),
                            len_non_disaster = len(non_disaster_tweets))

@app.route('/form', methods = ['GET'])
def form():
    return render_template('form.html')

@app.route('/class', methods = ['POST'])
def get_class():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        tweet = {"text" : request.get_json()}
        var_class = predict(tweet)
        result = {"class" : var_class} 

        return jsonify(result)
    else:
        tweet = {"text" : request.form.get("text")}
        var_class = predict(tweet)
        
        return render_template('predict.html', value=var_class)

def predict(tweet):
    transformed_tweet = transform(tweet, tags_set, vectorizer)
    X = np.array(list(transformed_tweet.values()))
    prediction = model.predict(X.reshape(1,-1))[0]
    if prediction >= threshold:
        return 1
    else:
        return 0

def get_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)
    
    tweets = []
    for tweet in api.search_tweets(q="naturaldisaster", lang="en"):
        tweets.append(tweet)
    return tweets
        

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=9696)
    app.run()