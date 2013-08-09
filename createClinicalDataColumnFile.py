from os import listdir
from os.path import isfile, join

# Update these values
mypath = 'mydata/' # The folder where your clinical data files are located
outfile = open('mydata_columns.txt', 'w') # The columns file that will be created
fileending = '.txt' # All columns from the files in folder 'mypath' with a filename ending in 'filending' will be included
#  -----

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for f in onlyfiles:
	if f.endswith(fileending):
		print(f)

outfile.write('Filename	Category Code	Column Number	Data Label	Data Label Source	Control Vocab Cd')

for f in onlyfiles:
	if f.endswith(fileending):
		infile = open(join(mypath,f));
		first_line = infile.readline()
		print(first_line)
		words = first_line.strip('\n').split('\t')
		i = 1
		for word in words:
			outfile.write('\n'+f+'\tCategory\t'+str(i))
			outfile.write('\t')
			outfile.write(word)
			outfile.write('\t\t')
			i += 1