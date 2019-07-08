
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
try:
    from threader import Threader
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

		if canTweet == False:
			sourceFile = 'C:\\Users\\mrbar\\Documents\\visual studio 2017\\Projects\\Birdfeeder\\Birdfeeder\\toTweet.txt'
			targetFile = 'C:\\Users\\mrbar\\Documents\\visual studio 2017\\Projects\\Birdfeeder\\Birdfeeder\\tweeted.txt'

		#Open feed file
		with open(sourceFile,'r') as f:
			wholeLine = f.readline()
			wholeLine = wholeLine.strip("\n")
		f.closed
		if wholeLine.strip() == "":
			print('nothing to tweet')
			return 0

        #Break up text into Tweet Thread
		threadParts = []
		threadCount = 0
		threadParts = ['']
		words = wholeLine.split(' ')
		for word in words:
			if len(threadParts[threadCount] + word) <= 140:
				threadParts[threadCount] = threadParts[threadCount] + ' ' + word
			else:
				threadCount = threadCount + 1
				threadParts.append(word)


		if canTweet:
			#api.update_status(status=wholeLine)
			th = Threader(tweets, api, wait=2)
			th.send_tweets()
		else:
			for threadPart in threadParts:
				print('TWEET: ' + threadPart)

		#open target file
		if os.path.exists(targetFile) == False:
			f = open(targetFile, 'w+')
			f.closed
		with open(targetFile, 'a') as f:
			fts = datetime.datetime.now().strftime('%a, %d/%B/%Y %I:%M%p')
			f.writelines(fts + ': ' + wholeLine + "\n")
		f.closed

		#Remove line from source
		tempfilename = '/media/usb/' + datetime.datetime.now().strftime('%Y%B%d%I%M') + '.txt'
		with open(sourceFile, "r") as input:
			with open(tempfilename, "w+") as output: 
				for line in input:
					if line.strip("\n") != wholeLine:
						output.write(line)
		os.remove(sourceFile)
		os.rename(tempfilename, sourceFile)

		return 1

	except BaseException as err:
		print('error:', err)
		return 0

#Main Code body
twConfig = ConfigParser()
fConfig = ConfigParser()
sConfig = ConfigParser()
twConfig.read('twitter.ini')
fConfig.read('files.ini')
sConfig.read('settings.ini')
secondsBetweenTweets = int(sConfig["birdfeederSettings"]["minutesBetweenTweets"]) * 60
while True:
	result = nextTweet()
	if(result == 0):
		break
	time.sleep(secondsBetweenTweets)