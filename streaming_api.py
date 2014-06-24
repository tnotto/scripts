import tweepy
import json

access_token_key = "423741663-xYSXlhYjtibfpys9bMmVi0WPlzkV9x88IQKX7aG1"
access_token_secret = "CAqCn0glCOTXwj6qb0Ps5MeexN614r3nhurPrmqE7TRBj"

consumer_key = "KhKZSHuVqmgWdItForr7ZQ"
consumer_secret = "3ezpH87yHfWrmBoRivYEmodMrFH0409L5kyAqwm0"

# consumer_key = ''
# consumer_secret = ''
# 
# access_token_key = ''
# access_token_secret = ''
# 
auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print tweet

    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return False

    def on_data(self, data):
        print json.loads(data)

    def on_timeout(self):
        return True

l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
#setTerms = ['hello', 'goodbye', 'goodnight', 'good morning']
# setTerms = ['@gigaom']
streamer.filter(track=['@gigaom'])
