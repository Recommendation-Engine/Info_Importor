import urllib, urllib2

class MovieInfoCrawler(object):

	def __init__(self, movieSource):
		self.__movieSource = movieSource

	def analyseMovie(self):
		with open(self.__movieSource, 'r') as inputfile:
			with open("data/result_2.txt",'w') as outputfile:
				for line in inputfile:
					items = line.split("::")
					movieId = int(items[0])

					categories = items[2].strip().split("|")
					movieQueries = self._generateMovieQuery(items[1])
					jsonString = ''
					for movieQuery in movieQueries:
						response = urllib2.urlopen("http://www.omdbapi.com/?" + movieQuery + "&plot=full&r=json")
						jsonString = response.read()
						if jsonString != '{"Response":"False","Error":"Movie not found!"}':
							break

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
		movieQueries = []
		for i in range(-1, 2):
			movieDict = {}
			movieDict['t'] = movieName
			movieDict['y'] = year - i
			movieQuery = urllib.urlencode(movieDict)
			movieQueries.append(movieQuery)

		return movieQueries

def main():
	importer = MovieInfoCrawler("data/errorfile.txt")
	importer.analyseMovie()

if __name__ == '__main__':
	main()
