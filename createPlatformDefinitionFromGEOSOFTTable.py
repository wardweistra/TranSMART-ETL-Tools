import argparse
from os.path import join

parser = argparse.ArgumentParser(description='Convert the SOFT table file (GPLxxxx.annot) from GEO to the platform file expected by tranSMART.')
parser.add_argument('platform', default='platform', help='The name of the platform.')
parser.add_argument('-organism', default='Homo Sapiens', help='The name of the organism.')
parser.add_argument('-infile', default='[platform].annot', help='The file to be used as an input. Will use [platform].annot if left emtpy.')
parser.add_argument('-folder', default='./', help='The folder for the in and output files.')
arguments = parser.parse_args()

gpl_id = arguments.platform
organism = arguments.organism

if (arguments.infile == '[platform].annot') :
	arguments.infile = arguments.platform+'.annot'

infile = open(join(arguments.folder,arguments.infile),'r')
outfile = open(join(arguments.folder,gpl_id+'-platform.txt'), 'w');

# Don't write this header line, contrary to some manuals. Will result in this error:
# 	"invalid input syntax for type numeric: "GENE_ID""
# outfile.write('GPL_ID\tPROBE_ID\tGENE_SYMBOL\tGENE_ID\tORGANISM')

inputheaderlineremoved = 0
thisthefirstoutputline = 1

for line in infile:
	if line[:1] not in ['!','^','#']:
		if inputheaderlineremoved == 0:
			inputheaderlineremoved = 1
		else:
			words = line.strip('\n').split('\t')

			probe_id = words[0]
			gene_symbol = words[2].split('///')[0]
			gene_id = words[3].split('///')[0]

			if thisthefirstoutputline:
				thisthefirstoutputline = 0
			else:
				outfile.write('\n')

			outfile.write(gpl_id+'\t'+probe_id+'\t'+gene_symbol+'\t'+gene_id+'\t\"'+organism+'\"')
