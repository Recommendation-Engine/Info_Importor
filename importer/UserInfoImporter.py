import json
from recommender.RecommendInterestToUser import *
class UserInfoImporter(object):

	def __init__(self,userInfoFile,userCatFile,ageCatFile,rating_file, movie_info_file, user_interest_file):
		self.__userInfoFile = userInfoFile
		self.__userCatFile = userCatFile
		self.__ageCatFile = ageCatFile
		self.__userCategory = []
		self.__ageCategory = {}
		self.__userInterests = {}
		self.importUserCategory()
		self.importAgeCategory()
		self.importUserInterests(rating_file, movie_info_file, user_interest_file)

	def importUserInterests(self, rating_file, movie_info_file, user_interest_file):
		RecommendInterestToUser(rating_file, movie_info_file, user_interest_file)
		with open(user_interest_file, 'r') as f:
			self.__userInterests = json.load(f)

	def importUserCategory(self):
		with open(self.__userCatFile,'r') as inputfile:
			for line in inputfile:
				self.__userCategory.append(line.split("\t")[1].strip())

	def _processAge(self, line):
		items = line.split("\t")
		ageId = int(items[0].strip())

		ageItems = items[1].split("-")
		ageRange = (int(ageItems[0]), int(ageItems[1]))

		return ageId, ageRange

	def importAgeCategory(self):
		with open(self.__ageCatFile,'r') as inputfile:
			for line in inputfile:
				ageId, ageRange = self._processAge(line)
				self.__ageCategory[ageId] = ageRange

	def _processUserInfo(self, line):
		items = line.split("::")
		uid = int(items[0].strip())
		user = {}
		user['uid'] = int(items[0].strip())
		user['gender'] = items[1].strip()
		user['age'] = self.__ageCategory[int(items[2].strip())]
		user['occupation'] = self.__userCategory[int(items[3].strip())]
		user['zipcode'] = items[4].strip()
		user['genre'] = self.__userInterests[items[0].strip()]['genre']

		return user

	def importUserInfo(self, collection):
		with open(self.__userInfoFile,'r') as inputfile:
			for line in inputfile:
				user = self._processUserInfo(line)
				_id = collection.insert_one(user).inserted_id
				if _id is None:
					print "line: " + line +" failed to insert into databse" 