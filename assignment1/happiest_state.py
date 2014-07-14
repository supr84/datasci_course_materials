
from operator import itemgetter
import sys
import json

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

inv_map = {}
for k, v in states.items():
        inv_map[v] = k

def getSentimentSocres(fp):
        afinnfile = open(fp)
        scores = {} # initialize an empty dictionary
        for line in afinnfile:
                term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
                scores[term] = int(score)  # Convert the score to an integer.
        return scores

def getTermsentiment(term, sentimentScores):
        if term in sentimentScores:
                return sentimentScores[term]
        else:
                return 0

def getTweetSentiment(tweet):
        scores = getSentimentSocres(sys.argv[1])
        terms = tweet.split(' ')
        sentiments = [getTermsentiment(term, scores) for term in terms]
        return sum(sentiments)

def getTweetLocAndSentiment(tweetObj):
        stateSentiments = ()
        tweetJson = json.loads(tweetObj)
        if 'text' in tweetJson:
                tweetText = tweetJson['text']
                tweetSentiment = getTweetSentiment(tweetText)
                key = 'place'
                if key in tweetJson:
                        place = tweetJson[key]
                        if place is not None and 'name' in place:                                
                                if place['name'] in inv_map:
                                        stateSentiments = (inv_map[place['name']], tweetSentiment)
                else:
                        print 'no location found'
        return stateSentiments

def getStateSentiments(stateSentiments):
        happiestStates = {}
        for stateSentiment in stateSentiments:
            if len(stateSentiment) > 0:
                state = stateSentiment[0]
                sentiment = stateSentiment[1]
                metric = (0,0)
                if state in happiestStates:
                    metric = happiestStates[state]
                newMetric = (metric[0] + sentiment, metric[1] + 1)
                happiestStates[state] = newMetric
        return happiestStates

def getHappiestState(stateSentiments):
    happiestStates = {}
    for state in stateSentiments:
        happiestStates[state] = stateSentiments[state][0]/stateSentiments[state][1]
    
    sortedStates = sorted(happiestStates.items(), key=itemgetter(1), reverse=True)
    topState = sortedStates[0]
    return topState[0]
    
def main():
        tweet_file = open(sys.argv[2])
        jsonTweets = tweet_file.readlines()
        stateSentiments = map(getTweetLocAndSentiment, jsonTweets)
        stateSentiments = getStateSentiments(stateSentiments)
        print(getHappiestState(stateSentiments))
if __name__ == '__main__':
    main()
