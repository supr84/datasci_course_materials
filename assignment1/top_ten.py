
import sys
import json
import operator
from operator import itemgetter

def getTopTenHashTags(hashTags):
	sortedHashTags = sorted(hashTags.items(), key=itemgetter(1), reverse=True)
	getTopTenHashTags = sortedHashTags[0:10]
	return getTopTenHashTags

def getHashTagText(hashTag):
	return hashTag['text']

def getHashTags(tweetObj):
	tweetJson = json.loads(tweetObj)
	if 'entities' in tweetJson:
		entities = tweetJson['entities']
		hashtags = map(getHashTagText, entities['hashtags'])
	return hashtags

def getTermFrequency(distribution):
	total = sum(distribution.values())
	for term in distribution.keys():
		print term + ' {0:.4f}'.format(float(distribution[term])/total)

def main():
	hashTagFrequency = {}
	tweet_file = open(sys.argv[1])
	jsonTweets = tweet_file.readlines()
	hashTags = reduce(operator.add, map(getHashTags, jsonTweets))
	
	for hashTag in hashTags:
		if hashTag not in hashTagFrequency:
			hashTagFrequency[hashTag] = 0
		hashTagFrequency[hashTag] += 1

	topTenHashTagFrequency = getTopTenHashTags(hashTagFrequency)

	for item in topTenHashTagFrequency:
		print "%s %d" % (item[0], item[1])

if __name__ == '__main__':
    main()
