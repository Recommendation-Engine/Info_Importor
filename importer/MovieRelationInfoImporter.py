import json

class MovieRelationInfoImporter(object):
	"""docstring for CalculateCategoriesInCommon"""
	def __init__(self, moviefile, ratingfile, movieNo):
		self.__moviefile = moviefile
		self.__ratingfile = ratingfile
		# self.__outfile = outfile
		self.__movieNo = movieNo
		self.__movie2cat = {}
		self.__movieInfo = {}
		self.__res = []
		self.importMovieInfo()
		self.importRating()

	def _processLine(self, line):
		items = line.split("::")
		userId = int(items[0])
		movieId = int(items[1])
		rating = int(items[2])

		return userId, movieId, rating

	def importRating(self):
		with open(self.__ratingfile, 'r') as f:
			for line in f:
				userId, movieId, rating = self._processLine(line)
				if rating > 3: # Cares only positive ones
					self.__movieInfo[movieId]['positive_users'].add(userId)


	def _splitIntoSet(self, line, delimiter):
		return set([x.strip() for x in line.split(delimiter)])

	def _getMovieInfo(self, lines):
		'''
		    TODO: In meta, genre and actors are in single string.
		    It is beter to split into lists in the future.
		'''
		movieInfo = {}
		originalItems = lines[0].split("::")
		print originalItems[0]
		movieInfo['mid'] = int(originalItems[0])
		movieInfo['cat'] = originalItems[-1].strip().split('|')
		movieInfo['meta'] = json.loads(lines[1].strip())
		movieInfo['meta']['Genre'] = set() if movieInfo['meta']['Genre'] == "N/A" \
											else self._splitIntoSet(movieInfo['meta']['Genre'], ',')
		movieInfo['meta']['Actors'] = set() if movieInfo['meta']['Actors'] == "N/A" \
											else self._splitIntoSet(movieInfo['meta']['Actors'], ',')
		movieInfo['meta']['Director'] = set() if movieInfo['meta']['Director'] == "N/A" \
											else self._splitIntoSet(movieInfo['meta']['Director'], ',')
		return movieInfo

	def importMovieInfo(self):
		with open(self.__moviefile, 'r') as inFile:
			lines = inFile.readlines()
			for i in range(len(lines)):
				if i % 3 == 0:
					movieInfo = self._getMovieInfo(lines[i:i+2])
					self.__movieInfo[movieInfo['mid']] = movieInfo['meta']
					self.__movieInfo[movieInfo['mid']]['positive_users'] = set()

					# _id = collection.insert_one(movieInfo).inserted_id
					# if _id is None:
					# 	print "line: " + line +" failed to insert into databse" 

	

	def _genJsonRes(self, i, j, commonCat, commonActor, commonDirector, ratioI, ratioJ):
		record1 = {'mid':i, 'mid2':j, 'ratio':ratioI, 'cat':list(commonCat), 'actor':list(commonActor), 'director':list(commonDirector)}
		record2 = {'mid':j, 'mid2':i, 'ratio':ratioJ, 'cat':list(commonCat), 'actor':list(commonActor), 'director':list(commonDirector)}
		self.__res.append(record1)
		self.__res.append(record2)

	def importRelationInfo(self, collection):
		# print 'No of positive users of movie 1:', len(self.__movieInfo[1]['positive_users'])
		# print 'Positive users of movie 1:'
		# print self.__movieInfo[1]['positive_users']
		# print 'No of positive users of movie 3114:', len(self.__movieInfo[3114]['positive_users'])
		# print 'Positive users of movie 3114:'
		# print self.__movieInfo[3114]['positive_users']
		# print 'user in common:'
		# print len(self.__movieInfo[1]['positive_users'].intersection(self.__movieInfo[3114]['positive_users']))
		# raw_input('Press any key to continue')
		# with open(self.__outfile, 'w') as f:
		for i in range(1, self.__movieNo+1):
			for j in range(i+1, self.__movieNo+1):
				if j % 100 == 0:
					print i, j
				if i in self.__movieInfo and j in self.__movieInfo:
					commonCat = self.__movieInfo[i]['Genre'].intersection(self.__movieInfo[j]['Genre'])
					commonActor = self.__movieInfo[i]['Actors'].intersection(self.__movieInfo[j]['Actors'])
					commonDirector = self.__movieInfo[i]['Director'].intersection(self.__movieInfo[j]['Director'])
					commonUser = self.__movieInfo[i]['positive_users'].intersection(self.__movieInfo[j]['positive_users'])
					commonPi = 0 if len(self.__movieInfo[i]['positive_users']) == 0 \
									else len(commonUser)*100/len(self.__movieInfo[i]['positive_users'])
					commonPj = 0 if len(self.__movieInfo[j]['positive_users']) == 0 \
									else len(commonUser)*100/len(self.__movieInfo[j]['positive_users'])
					self._genJsonRes(i, j, commonCat, commonActor, commonDirector, commonPi, commonPj)

		result = collection.insert_many(self.__res)
		if len(result.inserted_ids) == 0:
			print 'Write to mongodb failed'
					
def main():
	calCatInCommon = MovieRelationInfoImporter("../data/movieInfo.txt", 
		"../data/ratings.txt", "../data/InfoInCommon.txt", 3952)
	print "loadMovieFile..."
	calCatInCommon.importMovieInfo()
	print "importRating..."
	calCatInCommon.importRating()
	print "calInfoInCommon..."
	calCatInCommon.calInfoInCommon()

if __name__ == '__main__':
	main()			


		