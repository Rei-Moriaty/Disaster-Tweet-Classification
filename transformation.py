import re
import nltk
from textblob import TextBlob
import spacy
import collections
import numpy as np

stopwords = nltk.download('stopwords')

words = ["fire", "news", "disaster", "suicide bomber", "oil spill", "california wildfire"]

def preprocess_text(txt, flg_stem=False, flg_lemmatize=False, stopwords=None):
    txt = re.sub(r'[^\w\s]', '', str(txt).lower().strip())
    
    result_txt = txt.split()
    
    if stopwords is not None:
        result_txt = [word for word in result_txt if word not in stopwords]
    
    if flg_stem:
        ps = nltk.stem.PorterStemmer()
        result_txt = [ps.stem(word) for word in result_txt]
    
    if flg_lemmatize:
        lem = nltk.stem.WordNetLemmatizer()
        result_txt = [lem.lemmatize(word) for word in result_txt]
    
    txt = " ".join(result_txt)
    return txt

def utils_lst_count(lst):
    dic_counter = collections.Counter()
    for x in lst:
        dic_counter[x] += 1
    dic_counter = collections.OrderedDict( 
                     sorted(dic_counter.items(), 
                     key=lambda x: x[1], reverse=True))
    lst_count = [ {key:value} for key,value in dic_counter.items() ]
    return lst_count

def utils_ner_features(lst_dics_tuples, tag):
    if len(lst_dics_tuples) > 0:
        tag_type = []
        for dic_tuples in lst_dics_tuples:
            for tuple in dic_tuples:
                type, n = tuple[1], dic_tuples[tuple]
                tag_type = tag_type + [type]*n
                dic_counter = collections.Counter()
                for x in tag_type:
                    dic_counter[x] += 1
        return dic_counter[tag]
    else:
        return 0

def transform(tweet, tags_set, vectorizer):
    tweet["text"] = preprocess_text(tweet["text"])
    tweet["word_count"] = len(str(tweet["text"]).split(" "))
    tweet["char_count"] = sum(len(word) for word in str(tweet["text"]).split(" "))
    tweet["sentence_count"] = len(str(tweet["text"]).split("."))
    tweet["avg_word_length"] = tweet["char_count"] / tweet["word_count"]
    tweet["avg_sentence_length"] =  tweet["word_count"] / tweet["sentence_count"]
    tweet["sentiment"] = TextBlob(tweet["text"]).sentiment.polarity
    ner = spacy.load("en_core_web_sm")
    tweet["tags"] =  [(tag.text, tag.label_) for tag in ner(tweet["text"]).ents]
    tweet["tags"] = utils_lst_count(tweet["tags"])
    for feature in tags_set:
        tweet["tags_"+feature] = utils_ner_features(tweet["tags"], feature)
    # tweet = vectorizer.transform([tweet["text"]])
    vector = vectorizer.transform([tweet["text"]]).todense().tolist()[0]
    for i in range(len(words)):
        tweet[words[i]] = vector[i]
    del tweet['text']
    del tweet['tags']
    return tweet
