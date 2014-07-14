import oauth2 as oauth
import urllib2 as urllib
import json

# See assignment1.html instructions or README for how to get these credentials

api_key = "8ewzPT0ALhn69hwGK95LVkt0F"
api_secret = "iSbGROm8E9QjuNfqjxeMUJu2np2XP9FvIrUWXXwh1t33AxHFws"
access_token_key = "215615956-T987TnNjzXzdxPl4DzIrkYNaRyV4C4qiJG0pWWX1"
access_token_secret = "veJfFhXOlIopNxOSTwWkyoAtPRIAlr6y5r06AOGEcmnih"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json?lang=en&place.country_code=US"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    tweetJson = json.loads(line.strip())
    if 'text' in tweetJson and tweetJson['lang'] == 'en':
      print line.strip()

if __name__ == '__main__':
  fetchsamples()
