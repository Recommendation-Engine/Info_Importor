import numpy
from scipy.sparse import dok_matrix

from SimilarityCalculator import SimilarityCalculator

class RecommendMovieToMovie(object):

	def __init__(self, inputfile, userSize, movieSize):
		self.__similarityMatrix = None
		self.__sortedIndexMatrix = None
		self.__inputfile = inputfile
		self.__userSize = userSize
		self.__movieSize = movieSize
		self.__movieUserMatrix = dok_matrix((movieSize+1,userSize+1))

	def generateMovieMatrix(self):
		with open(self.__inputfile, 'r') as source:
			for line in source:
				userId, movieId, rating = self._processLine(line)

				self.__movieUserMatrix[movieId,userId] = (rating - 3)
	
	def calculateSimilarity(self):
		similarityCalculator = SimilarityCalculator(self.__movieUserMatrix)
		self.__similarityMatrix = similarityCalculator.calculateSimilarity()

	def sortNeighbours(self):
		self.__sortedIndexMatrix = self.__similarityMatrix.argsort()

	def _processLine(self,line):
		items = line.split("::")
		userId = int(items[0])
		movieId = int(items[1])
		rating = int(items[2])

		return userId, movieId, rating

	def getTopKMovies(self, k, movieId):
		topKMovie = self.__sortedIndexMatrix[movieId, self.__movieSize-k:self.__movieSize]
		
		return numpy.asarray(topKMovie).flatten()[::-1]

	def generateRecommendMatrix(self):
		self.generateMovieMatrix()
		self.calculateSimilarity()
		self.sortNeighbours()