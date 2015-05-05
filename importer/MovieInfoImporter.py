import json

class MovieInfoImporter(object):
	"""docstring for MovieInfoImporter"""
	def __init__(self, inputFile):
		self.__inputFile = inputFile

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
		return movieInfo

	def importMovieInfo(self, collection):
		with open(self.__inputFile, 'r') as inFile:
			lines = inFile.readlines()
			for i in range(len(lines)):
				if i % 3 == 0:
					movieInfo = self._getMovieInfo(lines[i:i+2])

					_id = collection.insert_one(movieInfo).inserted_id
					if _id is None:
						print "line: " + line +" failed to insert into databse" 
		