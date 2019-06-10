
import os.path
import datetime
import sys
import time
from configparser import ConfigParser

canTweet = True
try:
    from twython import Twython
except:
    canTweet = False

def nextTweet():
	try:
		if canTweet:
		    apiKey = twConfig['tokens']['apiKey']
		    apiSecret = twConfig['tokens']['apiSecret']
		    accessToken = twConfig['tokens']['accessToken']
		    accessTokenSecret = twConfig['tokens']['accessTokenSecret']
		    api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

		sourceFile = fConfig['files']['sourceFile']
		targetFile = fConfig['files']['targetFile']

		#Open feed file
		with open(sourceFile,'r') as f:
			tweetText = f.readline()
			tweetText = tweetText.strip("\n")
		f.closed
		if tweetText.strip() == "":
			print('nothing to tweet')
			quit()

		if canTweet:
			api.update_status(status=tweetText)
		else:
			print('TWEET: ' + tweetText)

		#open target file
		if os.path.exists(targetFile)==False:
			f = open(targetFile, 'w+')
			f.closed
		with open(targetFile, 'a') as f:
			fts = datetime.datetime.now().strftime('%a, %d/%B/%Y %I:%M%p')
			f.writelines(fts + ': ' + tweetText + "\n")
		f.closed

		#Remove line from source
		tempfilename = '/media/usb/' + datetime.datetime.now().strftime('%Y%B%d%I%M') + '.txt'
		with open(sourceFile, "r") as input:
			with open(tempfilename, "w+") as output: 
				for line in input:
					if line.strip("\n") != tweetText:
						output.write(line)
		os.remove(sourceFile)
		os.rename(tempfilename, sourceFile)

	except BaseException as err:
		print('error:', err)

#Main Code body
twConfig = ConfigParser()
fConfig = ConfigParser()
sConfig = ConfigParser()
twConfig.read('twitter.ini')
fConfig.read('files.ini')
sConfig.read('settings.ini')
secondsBetweenTweets = int(sConfig["birdfeederSettings"]["minutesBetweenTweets"])*60
while True:
	nextTweet()
	time.sleep(secondsBetweenTweets)