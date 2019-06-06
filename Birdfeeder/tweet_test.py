#!/usr/bin/env python
import sys
from twython import Twython

tweetStr = "This was sent from my pi...  I RULE!"

# your twitter consumer and access information goes here
# note: these are garbage strings and won't work
apiKey = 'YCoDZEBfVYDptrzvdsOzLJnww'
apiSecret = 'u6pfm5IIIXQy2z8K9Msx8LYFR2MVoFOjJMbVrPZBtW1cZugmvj'
accessToken = '1134849985269440513-1ZPjMVU1KbAiooHNpitovDPcDcX9bP'
accessTokenSecret = 'JL5x5Hf0Sa0RG5FfR6TwTq5HmluED9bf06QMmkUT3CT4i'

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

api.update_status(status=tweetStr)

print "Tweeted: " + tweetStr
