from os import listdir
from os.path import isfile, join
import sys, getopt

def createColumnFile(mypath, outfilename, fileending):
	outfile = open(outfilename, 'w') # The columns file that will be created

	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	outfile.write('Filename	Category Code	Column Number	Data Label	Data Label Source	Control Vocab Cd')

	print "Parsing files:"
	for f in onlyfiles:
		if f.endswith(fileending) and f not in (outfilename,'study_columns.txt'):
			print "-",f
			infile = open(join(mypath,f));
			first_line = infile.readline()
			words = first_line.strip('\n').split('\t')
			i = 1
			for word in words:
				outfile.write('\n'+f+'\tCategory\t'+str(i))
				outfile.write('\t')
				outfile.write(word)
				outfile.write('\t\t')
				i += 1

def usage():
	print 'Usage: '+sys.argv[0]+' [-f <folder>] [-o <columnsfilename>] [-e <extension>]'

def main(argv):
	# Default values
	mypath = '.' # The folder where your clinical data files are located
	outfilename = 'study_columns.txt' # The output column mapping file
	fileending = '.txt' # All columns from the files in folder 'mypath' with a filename ending in 'filending' will be included

	try:
		opts, args = getopt.getopt(argv,"hf:o:e:",["help","folder=","output=","extension="])
	except getopt.GetoptError:
		print "Unknown option"
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h','--help'):
			usage()
			sys.exit()
		elif opt in ("-f", "--folder"):
			mypath = arg
		elif opt in ("-o", "--output"):
			outfilename = arg
		elif opt in ("-e", "--extension"):
			fileending = arg
		else:
			print "Unknown option"
			usage()
			sys.exit()

	print 'Input folder:', mypath
	print 'Clinical data file extension:', fileending
	print 'Output column file:', outfilename

	createColumnFile(mypath, outfilename, fileending)

if __name__ == "__main__":
	main(sys.argv[1:])
