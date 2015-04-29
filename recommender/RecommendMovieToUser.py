import time
import numpy
from scipy.sparse import coo_matrix, dok_matrix

from SimilarityCalculator import SimilarityCalculator

class RecommendMovieToUser(object):

	def __init__(self, inputfile, userSize, movieSize):
		self.__similarityMatrix = None
		self.__sortedIndexMatrix = None
		self.__inputfile = inputfile
		self.__userSize = userSize
		self.__movieSize = movieSize
		self.__rating_avg = 0.0
		self.__userMovieMatrix = dok_matrix((userSize+1,movieSize+1))
		self.__userMovieOrigin = dok_matrix((userSize+1,movieSize+1))
		self.__userMovieBinary = dok_matrix((userSize+1,movieSize+1))
		self.__resultMatrix = None

	def generateMovieUserDict(self, k):
		self.generateUserMatrix()
		self.calculateSimilarity()
		self.sortNeighbours()
		self.generateRecommendMatrix(k)
		return self.getTopKMovies(100)

	def generateUserMatrix(self):
		with open(self.__inputfile, 'r') as source:
			rating_sum, count = 0.0, 0

			for line in source:
				userId, movieId, rating = self._processLine(line)

				self.__userMovieMatrix[userId,movieId] = (rating - 3)
				self.__userMovieOrigin[userId,movieId] = rating
				self.__userMovieBinary[userId,movieId] = 1

				rating_sum += rating
				count += 1

			self.__rating_avg = rating_sum/count
	
	def calculateSimilarity(self):
		similarityCalculator = SimilarityCalculator(self.__userMovieMatrix)
		self.__similarityMatrix = similarityCalculator.calculateSimilarity()

	def sortNeighbours(self):
		self.__sortedIndexMatrix = self.__similarityMatrix.argsort()

	def generateRecommendMatrix(self, k):		
		filter_matrix = self._generateFilterMatrix(k)

		dot_product_matrix = filter_matrix.dot(self.__userMovieOrigin).todense()
		size_matrix = filter_matrix.dot(self.__userMovieBinary).todense()
		res_matrix = numpy.divide(dot_product_matrix, size_matrix)
		
		res_matrix[numpy.isinf(res_matrix)] = self.__rating_avg
		res_matrix[numpy.isnan(res_matrix)] = self.__rating_avg

		self.__resultMatrix = res_matrix
		
	def getTopKMovies(self, k):
		topKMoviesDict = {}

		userMovieSorted = self.__resultMatrix.argsort()
		for user in range(1, self.__userSize+1):
			recommendedMovies = []

			for movie in reversed(range(1, self.__movieSize+1)):
				if self.__userMovieBinary[user, movie] != 1 and len(recommendedMovies) < k:
					recommendedMovies.append(userMovieSorted[user, movie])
					
			topKMoviesDict[user] = recommendedMovies

		return topKMoviesDict

	def _getTopKNeighboursForAll(self, k):
		return self.__sortedIndexMatrix[:, self.__userSize-k:self.__userSize]

	def _generateFilterMatrix(self, k):
		#Filter Matrix's size is usersize*usersize, (user, topKneighbour) = 1, otherwise = 0
		topKUsersAll = self._getTopKNeighboursForAll(k)

		xindex = numpy.zeros((self.__userSize+1, k))
		for i in range(1, self.__userSize+1):
			xindex[i,:] = i

		filter_matrix = coo_matrix((numpy.ones((self.__userSize+1)*k), 
			(xindex.flatten(), numpy.asarray(topKUsersAll).flatten())), 
			shape=(self.__userSize+1, self.__userSize+1))

		return filter_matrix

	def _processLine(self,line):
		items = line.split("::")
		userId = int(items[0])
		movieId = int(items[1])
		rating = int(items[2])

		return userId, movieId, rating
