from os.path import join

# Update these values
mypath = '.'
columnsfile = "mydata_columns.txt"
outfile = open('mydata_wordmap.txt', 'w');
#  -----

outfile.write('Filename	Column Number	Original Data Value	New Data Values')

infile = open(join(mypath,columnsfile));
infile.readline()
for line in infile:
	words = line.strip('\n').split('\t')
	outfile.write('\n'+words[0]+'\t'+words[2]+'\t'+'Old\tNew')
