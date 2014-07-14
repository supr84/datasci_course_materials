import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
print str(len(fp.readlines()))

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

def getNewTermSentimentScore(key, rawScores):
	pos = rawScores['pos']
	neg = rawScores['neg']
	sentiment = 0
	if len(pos) > len(neg):
		sentiment = sum(pos)
	elif len(pos) < len(neg):
		sentiment = sum(neg)
	return "%s %f" %(str(key), sentiment)

def main():
	newScores = {}
	scores = getSentimentSocres(sys.argv[1])
	tweet_file = open(sys.argv[2])
	jsonTweets = tweet_file.readlines()
	tweetTexts = map(getTweetText, jsonTweets)

	for tweetText in tweetTexts:
		tweetSentiment = getTweetSentiment(tweetText, scores)
		tweetTerms = tweetText.split(' ')
		for tweetTerm in tweetTerms:
			try:
				strTweetTerm = str(tweetTerm)
			except:
				continue
			if strTweetTerm in scores or len(strTweetTerm) < 2:
				continue
			elif strTweetTerm not in newScores:
				newScores[strTweetTerm] = {'pos':[], 'neg':[]}

			if tweetSentiment < 0:
				newScores[strTweetTerm]['neg'].append(tweetSentiment)
			if tweetSentiment > 0:
				newScores[strTweetTerm]['pos'].append(tweetSentiment)
	newTerms = newScores.keys()
	ops = [getNewTermSentimentScore(newTerm, newScores[newTerm]) for newTerm in newTerms]
	for op in ops:
		print op

if __name__ == '__main__':
    main()
