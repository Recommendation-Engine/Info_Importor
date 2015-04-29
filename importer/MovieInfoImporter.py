import urllib, urllib2

class MovieInfoImporter(object):

	def __init__(self, movieSource):
		self.__movieSource = movieSource

	def analyseMovie(self):
		with open(self.__movieSource, 'r') as inputfile:
			with open("result.txt",'w') as outputfile:
				for line in inputfile:
					items = line.split("::")
					movieId = int(items[0])
					movieQuery = self._generateMovieQuery(items[1])
					categories = items[2].strip().split("|")

					response = urllib2.urlopen("http://www.omdbapi.com/?" + movieQuery + "&plot=full&r=json")
					jsonString = response.read()

					print movieId
					outputfile.write(line + "\n" + jsonString + "\n")

	
	def _generateMovieQuery(self, movieInfo):
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

		movieDict = {}
		movieDict['t'] = movieName
		movieDict['y'] = year
		movieQuery = urllib.urlencode(movieDict)

		return movieQuery

def main():
	importer = MovieInfoImporter("../data/movies.txt")
	importer.analyseMovie()

if __name__ == '__main__':
	main()