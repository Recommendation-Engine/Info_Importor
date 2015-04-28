from UserInfoImportor import UserInfoImportor
from OriginalRatingImportor import OriginalRatingImportor
from pymongo import MongoClient

class Importor(object):

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
	importor = Importor('localhost', 27017, 'recommendation_engine')
	db = importor.connectMongoDB()

	userInfoImportor = UserInfoImportor("data/users.txt", "data/UserCategory.txt", "data/AgeCategory.txt")
	userInfoImportor.importUserInfo(db['users'])

	originalRatingImportor = OriginalRatingImportor("data/ratings.txt")
	originalRatingImportor.importRating(db["ratings"])

	importor.closeDB()

if __name__ == '__main__':
	main()