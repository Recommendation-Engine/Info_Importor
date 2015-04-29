from importer.UserInfoImporter import *
from importer.OriginalRatingImporter import *
from importer.MovieMovieMatrixImporter import *
from importer.MovieUserMatrixImporter import *

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

	movieUserMatrixImporter = MovieUserMatrixImporter("data/ratings.txt", 6040, 3952)
	movieUserMatrixImporter.importMatrix(db['m2u'])

	print "hahahahahhahahhhh"

	movieMovieMatrixImporter = MovieMovieMatrixImporter("data/ratings.txt", 6040, 3952)
	movieMovieMatrixImporter.importMatrix(db["m2m"])

	userInfoImporter = UserInfoImporter("data/users.txt", "data/UserCategory.txt", "data/AgeCategory.txt")
	userInfoImporter.importUserInfo(db["users"])

	originalRatingImporter = OriginalRatingImporter("data/ratings.txt")
	originalRatingImporter.importRating(db["ratings"])

	importer.closeDB()

if __name__ == '__main__':
	main()