import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
	return fp.readlines()

def getTermsentiment(term, sentimentScores):
	if term in sentimentScores:
		return sentimentScores[term]
	else:
		return 0

def getTweetSentiment(tweet, scores):
	terms = tweet.split(' ')
	sentiments = [getTermsentiment(term, scores) for term in terms]
	return sum(sentiments)

def getTweetText(tweetObj):
	tweetText = ''
	tweetJson = json.loads(tweetObj)
	if 'text' in tweetJson:
		tweetText = tweetJson['text']
	return tweetText

def getSentimentSocres(fp):
	afinnfile = open(fp)
	scores = {} # initialize an empty dictionary
	for line in afinnfile:
  		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  		scores[term] = int(score)  # Convert the score to an integer.
	return scores

def main():
    tweet_file = open(sys.argv[2])
    scores = getSentimentSocres(sys.argv[1])
    jsonTweets = lines(tweet_file)
    tweetTexts = map(getTweetText, jsonTweets)
    tweetSentiments = [getTweetSentiment(tweetText, scores) for tweetText in tweetTexts]
    for tweetSentiment in tweetSentiments:
    	print(tweetSentiment)

if __name__ == '__main__':
    main()
