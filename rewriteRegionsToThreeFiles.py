import argparse
from os.path import join

parser = argparse.ArgumentParser(description='Split the regions.tsv file from Chipster aCGH workflow into the three files expected by tranSMART.')
parser.add_argument('infile', default='regions.txt', help='The regions file to be used as an input.')
parser.add_argument('platform', default='platform', help='The name of the platform.')
parser.add_argument('study', default='study', help='The name of the study.')
parser.add_argument('-folder', default='./', help='The folder for the in and output files.')
parser.add_argument('-level', default='region', choices=['region', 'gene'], help='The aggregation level of the data.')
parser.add_argument('-tissue', default='', help='The tissue from which the samples come.')
arguments = parser.parse_args()

infile = open(join(arguments.folder,arguments.infile),'r')
platformdefinitionfile = open(join(arguments.folder,arguments.platform+'_'+arguments.level+'_platform.txt'), 'w');
subjectmappingfile = open(join(arguments.folder,arguments.study+'_subjectmapping.txt'), 'w');
samplesfile = open(join(arguments.folder,arguments.study+'_samples.txt'), 'w');

subjects = {}

# Write header for samplesfile and collect subjects for subjectmappingfile
firstlinewords = infile.readline().strip('\n').split('\t')
samplesfile.write(arguments.level+'_id')

order = ['chip','segm','flag','loss','norm','gain','amp']

# Set first header name to be 1 if the first column has no header
# columnnr = 0
columnnr = 1

for word in firstlinewords:
	if word not in ['chromosome','start','end','symbol','type','cytoband','strand','num.probes','loss.freq','gain.freq','amp.freq','cnv.count','cnv.proportion']:
		parts = word.split('.')
		#subject = parts[1]+'-'+parts[2]+'-'+parts[3]

		column = parts[0]
		# Map input names to output names
		if column == 'segmented':
			column = 'segm'
		elif column == 'probloss':
			column = 'loss'
		elif column == 'probnorm':
			column = 'norm'
		elif column == 'probgain':
			column = 'gain'
		if column in order:
			subject = parts[1]
			if subject not in subjects:
				subjects[subject] = {}
			subjects[subject][column] = columnnr

	columnnr += 1

for subject in subjects:
	for column in order:
		if column in subjects[subject]:
			samplesfile.write('\t'+subject+'.'+column)
		else:
			samplesfile.write('\t'+subject+'.'+column)


# Write subjectmappingfile
subjectmappingfile.write('STUDY_ID\tSITE_ID\tSUBJECT_ID\tSAMPLE_ID\tPLATFORM\tTISSUETYPE\tATTR1\tATTR2\tCATEGORY_CD\tSOURCE_CD')
for subject in subjects:
	subjectmappingfile.write('\n'+arguments.study+'\t\t'+subject+'\t'+subject+'\t'+arguments.platform+'\t'+arguments.tissue+'\t\t\tBiomarker_Data+Chrom+PLATFORM+TISSUETYPE\tSTD')
	# Do we need another tab after this like in the gene expression?
	# What is SITE_ID = 2?

# Write header for platformdefinitionfile
platformdefinitionfile.write('GPL_ID\tREGION_NAME\tCHROMOSOME\tSTART_BP\tEND_BP\tNUM_PROBES\tCYTOBAND\tGENE_SYMBOL\tGENE_ID\tORGANISM')

# For ever line in infile make a line in the platformdefinitionfile and the samples file
for line in infile:
	words = line.strip('\n').split('\t')
	chromosome = words[1]
	start = words[2]
	end = words[3]

	# Write the region name
	if arguments.level == 'region':
		# Get regions name
		numprobes = words[4]
		cytoband = ''
		gene_symbol = ''
		gene_id = ''
		regionname = 'chr'+chromosome+':'+start+'-'+end
	elif arguments.level == 'gene':
		numprobes = ''
		cytoband = words[6]
		gene_symbol = words[4]
		gene_id = ''
		regionname = words[0]
	samplesfile.write('\n'+regionname)
	
	# Write the values
	for subject in subjects:
		for column in order:
			if column in subjects[subject]:
				columnnr = subjects[subject][column]
				samplesfile.write('\t'+words[columnnr])
			else:
				samplesfile.write('\t0')

	# for word in words[8:]:
	# 	samplesfile.write('\t'+word)
	
	# Write region definition
	platformdefinitionfile.write('\n'+arguments.platform+'\t'+regionname+'\t'+chromosome+'\t'+start+'\t'+end+'\t'+numprobes+'\t'+cytoband+'\t'+gene_symbol+'\t'+gene_id+'\tHomo Sapiens')