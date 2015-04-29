from recommender.RecommendMovieToMovie import *

class MovieMovieMatrixImporter(object):

	def __init__(self, inputfile, userSize, movieSize):
		self.__recommender = RecommendMovieToMovie(inputfile, userSize, movieSize)
		self.__movieSize = movieSize

	def _generateMovieList(self, movieId):
		movies = {}
		movies['mid'] = movieId
		movies['movies'] = self.__recommender.getTopKMovies(100, movieId).tolist()

		return movies
	
	def importMatrix(self, collection):
		self.__recommender.generateRecommendMatrix()

		for movieId in range(1, self.__movieSize+1):
			movies = self._generateMovieList(movieId)

			_id = collection.insert_one(movies).inserted_id
			if _id is None:
				print "line: " + line +" failed to insert into databse" 

