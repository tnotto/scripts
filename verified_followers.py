
import oauth2 as oauth
import urllib2
import json
from time import sleep


def access_tokens():
    """
    access tokens for twitter
    """
    Twitter_access_token_key = "487988395-ukV6GDNqeFStakH0v9fomzYOxNEkDzBbjaZ33AyS"
    Twitter_access_token_secret = "w75CWasEEng6xyh3WmpNSuhQYMXgvxcAiZVSVxSKmsIrA"

    Twitter_consumer_key = "f6PXlf2hCwDg9U4P9LP6sotyt"
    Twitter_consumer_secret = "UTkvbwqMBsAX0HAV6et3QstCMQ5SBhDVndfIb2nroQmHFMxae9"

    return ({'twitter_access_token_key':Twitter_access_token_key,
        'twitter_access_token_secret': Twitter_access_token_secret,
        'twitter_consumer_key':Twitter_consumer_key,
        'twitter_consumer_secret':Twitter_consumer_secret
        })

def twitterreq(Url):
    """
    Makes the calls to twitter API
    """
    Access_token_key = access_tokens()['twitter_access_token_key']
    Access_token_secret = access_tokens()['twitter_access_token_secret']

    Consumer_key = access_tokens()['twitter_consumer_key']
    Consumer_secret = access_tokens()['twitter_consumer_secret']

    Parameters = []

    _debug = 0

    Oauth_token = oauth.Token(key=Access_token_key, secret=Access_token_secret)
    Oauth_consumer = oauth.Consumer(key=Consumer_key, secret=Consumer_secret)

    Signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    Http_method = "GET"

    Http_handler = urllib2.HTTPHandler(debuglevel=_debug)
    Https_handler = urllib2.HTTPSHandler(debuglevel=_debug)

    Req = oauth.Request.from_consumer_and_token(Oauth_consumer,
                                             token=Oauth_token,
                                             http_method=Http_method,
                                             http_url=Url,
                                             parameters=Parameters)

    Req.sign_request(Signature_method_hmac_sha1, Oauth_consumer, Oauth_token)

    Encoded_post_data = None
    Url = Req.to_url()

    Opener = urllib2.OpenerDirector()
    Opener.add_handler(Http_handler)
    Opener.add_handler(Https_handler)
    Response = Opener.open(Url, Encoded_post_data)

    return Response

def followers_list(cursor='-1'):    

    Url = "https://api.twitter.com/1.1/followers/list.json?screen_name=sqor&cursor="+cursor
    Response = twitterreq(Url)

    return json.loads(Response.read())

def get_cursor(Data):
    
    return Data.get('next_cursor_str')

def is_verified(Data):

    if Data['verified']:
        print Data['screen_name']
        return Data['screen_name']
    else:
        return None

def get_verified_followers():

    Verified_users = []

    Cursor = '-1'
    while Cursor:
        follower_call = followers_list(Cursor)
        follower_list = follower_call['users']
        for User in follower_list:
            User_name = is_verified(User)
            Verified_users.append(User_name)

        Cursor = get_cursor(follower_call)    
        sleep(60)


    return Verified_users





    
