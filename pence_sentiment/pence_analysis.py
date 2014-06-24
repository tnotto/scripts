import json
import requests
import nltk
import re
import pickle

post_ids = ['804326526258715']
base_url = 'https://graph.facebook.com/v1.0/%s/comments?limit=100'
cap_tokenizer = nltk.RegexpTokenizer('[A-Za-z]\w+')

for post_id in post_ids:
    url = base_url % post_id
    r = requests.get(url)
    data = json.loads(r.content)
    comments_raw = [x['message'] for x in data['data']]

    keywords = []

    for comment in comments_raw:
        list_of_words = cap_tokenizer.tokenize(re.sub(r"(?:\@|https?\://)\S+", "", comment))
        keywords.append(dict([(word.lower(), True) for word in list_of_words]))

with open('sentiment.pickle') as f:
    classifier = pickle.load(f)

for post in keywords:
    val = classifier.classify(post)
    print post, val
