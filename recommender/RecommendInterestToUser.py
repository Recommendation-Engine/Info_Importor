import json
import operator

class RecommendInterestToUser(object):
	def __init__(self, rating_file, movie_info_file, output_file):
		self.__rating_file = rating_file
		self.__movie_info_file = movie_info_file
		self.__output_file = output_file
		self.__movie_info = {}
		self.__user_interests = {}
		self.__user_actors = {}
		self.importMovieInfo()
		self.calUserInterests()
		self.getTopInterests()

	def calUserInterests(self):
		with open(self.__rating_file, 'r') as source:
			for line in source:
				userId, movieId, rating = self._processLine(line)
				# if rating <= 3:
				# 	continue
				genres = self.__movie_info[movieId]['genre']
				actors = self.__movie_info[movieId]['actor']
				if userId not in self.__user_interests:
					self.__user_interests[userId] = {}
					self.__user_interests[userId]['genre'] = {}
					self.__user_interests[userId]['actor'] = {}
				for genre in genres:
					if genre not in self.__user_interests[userId]['genre']:
						self.__user_interests[userId]['genre'][genre] = 0
					self.__user_interests[userId]['genre'][genre] += 1
				for actor in actors:
					if actor not in self.__user_interests[userId]['actor']:
						self.__user_interests[userId]['actor'][actor] = 0
					self.__user_interests[userId]['actor'][actor] += 1


	def getTopInterests(self):
		for userId in self.__user_interests:
			interests = self.__user_interests[userId]
			sorted_genres = sorted(interests['genre'].items(), key=operator.itemgetter(1), reverse=True)
			sorted_actors = sorted(interests['actor'].items(), key=operator.itemgetter(1), reverse=True)
			self.__user_interests[userId]['genre'] = []
			self.__user_interests[userId]['actor'] = []
			for genre in sorted_genres:
				self.__user_interests[userId]['genre'].append({"name":genre[0],"weight":genre[1]})
			self.__user_interests[userId]['actor'] = []
			for actor in sorted_actors:
				self.__user_interests[userId]['actor'].append({"name":actor[0],"weight":actor[1]})
			# print userId, sorted_genres
			# print userId, sorted_actors
		with open(self.__output_file, 'w') as f:
			f.write(json.dumps(self.__user_interests))


	def _processLine(self,line):
		items = line.split("::")
		userId = int(items[0])
		movieId = int(items[1])
		rating = int(items[2])
		return userId, movieId, rating

	def _getMovieInfo(self, lines):
		movieInfo = {}
		originalItems = lines[0].split("::")
		movieInfo['mid'] = int(originalItems[0])
		meta = json.loads(lines[1].strip())
		meta_genre = meta['Genre'].split(',')
		meta_actor = meta['Actors'].split(',')
		movieInfo['genre'] = [genre.strip() for genre in meta_genre]
		movieInfo['actor'] = [actor.strip() for actor in meta_actor]
		return movieInfo

	def importMovieInfo(self):
		with open(self.__movie_info_file, 'r') as inFile:
			lines = inFile.readlines()
			for i in range(len(lines)):
				if i % 3 == 0:
					movieInfo = self._getMovieInfo(lines[i:i+2])
					self.__movie_info[movieInfo['mid']] = movieInfo

def main():
	RecommendInterestToUser("../data/ratings.txt", "../data/movieInfo.txt")

if __name__ == '__main__':
	main()
