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

#firstlinewords = infile.readline().strip('\n').split('\t')
outfile.write('GPL_ID\tPROBE_ID\tGENE_SYMBOL\tGENE_ID\tORGANISM')

firstlineremoved = 0

for line in infile:
	if line[:1] not in ['!','^','#']:
		if firstlineremoved == 0:
			firstlineremoved = 1
		else:
			words = line.strip('\n').split('\t')
			outfile.write('\n'+gpl_id+'\t'+words[0]+'\t'+words[2].split('///')[0]+'\t'+words[3].split('///')[0]+'\t\"'+organism+'\"')
