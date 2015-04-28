class UserInfoImportor(object):

	def __init__(self,userInfoFile,userCatFile,ageCatFile):
		self.__userInfoFile = userInfoFile
		self.__userCatFile = userCatFile
		self.__ageCatFile = ageCatFile
		self.__userCategory = []
		self.__ageCategory = {}
		self.importUserCategory()
		self.importAgeCategory()

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
		
		user = {}
		user['userId'] = int(items[0].strip())
		user['gender'] = items[1].strip()
		user['age'] = self.__ageCategory[int(items[2].strip())]
		user['occupation'] = self.__userCategory[int(items[3].strip())]
		user['zipcode'] = items[4].strip()

		return user

	def importUserInfo(self, collection):
		with open(self.__userInfoFile,'r') as inputfile:
			for line in inputfile:
				user = self._processUserInfo(line)
				_id = collection.insert_one(user).inserted_id
				if _id is None:
					print "line: " + line +" failed to insert into databse" 