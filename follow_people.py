import json
import tweepy
import time

handles = []
with open('All_handles.json', 'r') as handle_data:
    for line in json.loads(handle_data.read()):
        # print line
        if line['twitter_handle'] != "":
            handles.append(line['twitter_handle'])

Twitter_access_token_key = "2432702989-MPAJ0DygoEuC5ZGuaHlU57Wq6PQjFfn8Gt1K3vM"
Twitter_access_token_secret = "96hVkkNIaQU14zewJRX7WFI84zIe4XxnC2aPZORbAxvio"

Twitter_consumer_key = "UiCf8Qr8sKF9i3WCZfDmdi3ek"
Twitter_consumer_secret = "5xwxlDbG16a2IUv2TIlCjIUllewtlilCBsZVYA8FvYbBjrb0oN"

auth = tweepy.OAuthHandler(Twitter_consumer_key, Twitter_consumer_secret)
auth.set_access_token(Twitter_access_token_key, Twitter_access_token_secret)

api = tweepy.API(auth)
# print api.rate_limit_status()

for handle in handles:
    time.sleep(1)    
    try:
        api.create_friendship(str(handle))
        print 'yeah'
    except:
        print handle
        pass
