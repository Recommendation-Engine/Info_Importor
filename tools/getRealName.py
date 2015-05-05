 # -*- coding: utf-8 -*-
import json
import urllib, urllib2

def generateMovieQuery(movieInfo):
		items = movieInfo.split(" ")
		movieNameList = items[:-1]
		year = int(items[-1][1:-1])
		movieName = ''
		for item in movieNameList:
			if item[0] == "(" :
				break
			elif item[-1] == ",":
				movieName += (" " + item[:-1])
				break
			else:
				movieName += (" " + item)
		movieQueries = []
		movieDict = {}
		movieDict['q'] = movieName
		movieQuery = urllib.urlencode(movieDict)

		return movieQuery, movieNameList, year

def main():
	inputFile = 'data/errorfile_2.txt'
	outputFile = 'data/errorfile_2_modified.txt'
	with open(inputFile, 'r') as inFile:
		with open(outputFile, 'w') as ouFile:
			for line in inFile:
				items = line.split("::")

				#movieName = items[-2].split(' (')[0]

				movieQuery, movieNameList, year = generateMovieQuery(items[1])
				response = urllib2.urlopen('http://www.imdb.com/xml/find?json=1&nr=1&tt=on&' + movieQuery)

				jsonString = response.read()
				print jsonString
				if jsonString != '{}':
					jsonDict = json.loads(jsonString)

					print jsonDict
					if 'title_substring' in jsonDict and len(jsonDict['title_substring']) > 0:
						movieDict = jsonDict['title_substring'][0]
						realName = movieDict['title']
						newYear = movieDict['description'].split(',')[0]

						titleString = items[0] + '::' +  realName + '('+items[1].split('(')[0]+')'\
							+'('+str(year)+')' + ' ('  + str(newYear) + ')::' + items[-1]
						ouFile.write( titleString + '\n')
						continue
				ouFile.write(line)


if __name__ == '__main__':
	main()
