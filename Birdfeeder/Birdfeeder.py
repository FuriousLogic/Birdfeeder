
import os.path
import datetime
import sys
import time
from twython import Twython

def nextTweet():
	try:
		apiKey = 'YCoDZEBfVYDptrzvdsOzLJnww'
		apiSecret = 'u6pfm5IIIXQy2z8K9Msx8LYFR2MVoFOjJMbVrPZBtW1cZugmvj'
		accessToken = '1134849985269440513-1ZPjMVU1KbAiooHNpitovDPcDcX9bP'
		accessTokenSecret = 'JL5x5Hf0Sa0RG5FfR6TwTq5HmluED9bf06QMmkUT3CT4i'
		api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

		sourceFile = 'toTweet.txt'
		targetFile = 'tweeted.txt'

		#Open feed file
		with open(sourceFile,'r') as f:
			tweetText = f.readline()
			tweetText = tweetText.strip("\n")
		f.closed
		if tweetText.strip() == "":
			print('nothing to tweet')
			quit()

		api.update_status(status=tweetText)

		#open target file
		if os.path.exists(targetFile)==False:
			f = open(targetFile, 'w+')
			f.closed
		with open(targetFile, 'a') as f:
			fts = datetime.datetime.now().strftime('%a, %d/%B/%Y %I:%M%p')
			f.writelines(fts + ': ' + tweetText + "\n")
		f.closed

		#Remove line from source
		tempfilename = datetime.datetime.now().strftime('%Y%B%d%I%M') + '.txt'
		with open(sourceFile, "r") as input:
			with open(tempfilename, "w+") as output: 
				for line in input:
					if line.strip("\n") != tweetText:
						output.write(line)
		os.remove(sourceFile)
		os.rename(tempfilename, sourceFile)

	except BaseException as err:
		print('error:', err)

while True:
	nextTweet()
	time.sleep(600)