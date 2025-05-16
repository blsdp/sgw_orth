import argparse
import Levenshtein

def compare(file1, file2):
	with open(file1, 'r') as file1, open(file2, 'r') as file2:
		file1txt = file1.read()
		file2txt = file2.read()
		print(Levenshtein.distance(file1txt,file2txt))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='report Levenshtein edit distance between two files')
	parser.add_argument('file1', help='text file #1')
	parser.add_argument('file2', help='text file #2')
	args = parser.parse_args()

	if args.file1 and args.file2:
		compare(args.file1, args.file2)