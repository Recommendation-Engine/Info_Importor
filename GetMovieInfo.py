import urllib2
def main():
	with open('data/movies.txt', 'r') as f:
		for line in f:
			items = line.split('::')
			movieName = items[1]
	response = urllib2.urlopen('http://www.example.com/')
	html = response.read()
if __name__ == '__main__':
	main()