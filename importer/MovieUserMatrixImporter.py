from recommender.RecommendMovieToUser import *

class MovieUserMatrixImporter(object):

	def __init__(self, inputfile, userSize, movieSize):
		self.__recommender = RecommendMovieToUser(inputfile, userSize, movieSize)

	def importMatrix(self, collection):
		movieUserDict = self.__recommender.generateMovieUserDict(450)

		for user in movieUserDict:
			userDict = {}
			userDict["uid"] = user
			userDict["movies"] = movieUserDict[user]

			_id = collection.insert_one(userDict).inserted_id
			if _id is None:
				print "line: " + line +" failed to insert into databse" 