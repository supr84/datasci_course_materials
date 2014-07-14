
import sys
import json

def getTweetText(tweetObj):
	tweetText = ''
	tweetJson = json.loads(tweetObj)
	if 'text' in tweetJson:
		tweetText = tweetJson['text']
	return tweetText

def getTermFrequency(distribution):
	tf = {}
	total = sum(distribution.values())
	for term in distribution.keys():
		tf[term] = float(distribution[term])/total
	return tf

def isAlphabet(charecter):
	isCaps = 65 <= ord(charecter) and ord(charecter) <= 90
	isSmall =  97 <= ord(charecter) and ord(charecter) <= 122
	return isCaps or isSmall

def hasSpecialCharecters(term):
	return all(isAlphabet(c) for c in term)

def main():
	tweet_file = open(sys.argv[1])
	jsonTweets = tweet_file.readlines()
	tweetTexts = map(getTweetText, jsonTweets)
	freq = {}
	for tweetText in tweetTexts:
		terms = tweetText.split(' ')
		for term in terms:
			try:
				strTerm = str(term)
			except:
				continue
			if len(strTerm) < 2:
				continue
			if strTerm not in freq:
				freq[strTerm] = 1
			else:
				freq[strTerm] += 1
	tfs = getTermFrequency(freq)
	for term in tfs.keys():
		if hasSpecialCharecters(term) is True:
			print "%s %.4f" % (term, tfs[term])
if __name__ == '__main__':
    main()
