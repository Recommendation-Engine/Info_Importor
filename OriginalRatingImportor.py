from datetime import datetime

class OriginalRatingImportor(object):

	def __init__(self,ratingFile):
		self.__ratingFile = ratingFile

	def _processRating(self, line):
		items = line.split("::")
		
		rating = {}
		rating['userId'] = int(items[0].strip())
		rating['movieId'] = int(items[1].strip())
		rating['rating'] = int(items[2].strip())
		rating['datetime'] = datetime.fromtimestamp(int(items[3].strip()))

		return rating
	
	def importRating(self, collection):
		with open(self.__ratingFile, 'r') as inputfile:
			for line in inputfile:
				rating = self._processRating(line)
				_id = collection.insert_one(rating).inserted_id
				if _id is None:
					print "line: " + line +" failed to insert into databse" 