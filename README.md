# Disaster Tweet Classification


Twitter has become an important communication channel in times of emergency.
The ubiquitousness of smartphones enables people to announce an emergency they’re observing in real-time. Because of this, more agencies are interested in programatically monitoring Twitter (i.e. disaster relief organizations and news agencies).

But, it’s not always clear whether a person’s words are actually announcing a disaster. A tweet could sount like disaster but it would actually just be exclamation of the scenic beauty like the one below

"https://twitter.com/anyotherannak/status/629195955506708480"

So to overcome this problem I have made which will take the tweet text and classify it has disaster or non disater tweet and then served it as an webapp. 

In the home page the the app takes some tweets in the from twitter and classifies it has disaster or non disaster in real time. Another page gives us a form where we can enter tweet text and it can classify as disaster or non disaster tweet.


For EDA we first clean up the text remove stop words and do lemmatization.

After that we extract basic features such as word length, sentence count etc.


Then we extract some advance features like sentiment

After that using spacy we get some tags and based on these tags we create new features.

After that we get most frequent words for disaster tweets and use count vectorizer to get some new features based on this.


Also we test different algorithms based on accuracy and auc metric. We select 2 best algorithms.

After that we do hyperparameter tuning based on GridSearchCV and then based on ROC metrics we select Random Forest Classifier.


For threshold we select it based on True Positive Rate and False Positive Rate.


Then for deployment we create a flask app which takes real time tweets using tweepy and classify them as disaster or non disaster tweets. We also use waitress to serve the app. 


We then create Dockerfile to create containerize the app and use it


[![Disaster Tweet Classifier](https://imgur.com/G17dVYY)](https://youtu.be/99cM8lVPtrU)
[![Watch the video](https://i.imgur.com/vKb2F1B.png)](https://youtu.be/vt5fpE0bzSY)

