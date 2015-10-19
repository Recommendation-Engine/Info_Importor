from importer.UserInfoImporter import *
from importer.OriginalRatingImporter import *
from importer.MovieMovieMatrixImporter import *
from importer.MovieUserMatrixImporter import *
from importer.MovieInfoImporter import *
from importer.MovieRelationInfoImporter import *

from pymongo import MongoClient

class Importer(object):

	def __init__(self, host, port, dbName):
		self.__host = host
		self.__port = port
		self.__dbName = dbName

	def connectMongoDB(self):
		self.__client = MongoClient(self.__host, self.__port)

		return self.__client[self.__dbName]

	def closeDB(self):
		self.__client.close()

def main():
	importer = Importer('localhost', 27017, 'recommendation_engine')
	db = importer.connectMongoDB()

	# movieInfoImporter = MovieInfoImporter("data/movieInfo.txt")
	# movieInfoImporter.importMovieInfo(db["movies"])

	# print "hahahahahhahahhhh"

	# movieUserMatrixImporter = MovieUserMatrixImporter("data/ratings.txt", 6040, 3952)
	# movieUserMatrixImporter.importMatrix(db['m2u'])

	# movieMovieMatrixImporter = MovieMovieMatrixImporter("data/ratings.txt", 6040, 3952)
	# movieMovieMatrixImporter.importMatrix(db["m2m"])

	userInfoImporter = UserInfoImporter("data/users.txt", "data/UserCategory.txt", 
		"data/AgeCategory.txt", "data/ratings.txt", "data/movieInfo.txt", "data/userInterests.txt")
	userInfoImporter.importUserInfo(db["users"])

	# originalRatingImporter = OriginalRatingImporter("data/ratings.txt")
	# originalRatingImporter.importRating(db["ratings"])

	# movieRelationInfoImporter = MovieRelationInfoImporter("data/movieInfo.txt", 
	# 	"data/ratings.txt", 3952)
	# movieRelationInfoImporter.importRelationInfo(db["relation"])

	importer.closeDB()

if __name__ == '__main__':
	main()