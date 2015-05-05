def main():
	inputFile = 'data/result.txt'
	errorFile = 'data/errorfile.txt'
	successFile = 'data/successfile.txt'
	with open(inputFile, 'r') as inFile:
		with open(successFile, 'w') as suFile:
			with open(errorFile, 'w') as erFile:
				lines = inFile.readlines()
				for i in range(len(lines)):
					if i % 3 == 0:
						title_line = lines[i]
						result_line = lines[i+2]
						if result_line.strip() == '{"Response":"False","Error":"Movie not found!"}':
							erFile.write(title_line+'')
						else:
							suFile.write(title_line+'')
							suFile.write(result_line+'\n')

if __name__ == '__main__':
	main()