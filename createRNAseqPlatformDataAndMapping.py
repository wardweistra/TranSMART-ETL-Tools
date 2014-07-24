import argparse
from os.path import join

parser = argparse.ArgumentParser(description='Convert multiple RNAseq output files to the RNAseq platform, data file and subject sample mapping tranSMART expects.')
parser.add_argument('-infiles', required=True, nargs='*', help='The files to be used as input.')
parser.add_argument('-samples', required=True, nargs='*', help='The sample names to be used.')
parser.add_argument('-subjects', nargs='*', help='The subject names to be used. If empty the sample names will be used.')
parser.add_argument('-tissues', nargs='*', help='The tissue types to be used.')
parser.add_argument('-readcountcolumn', nargs='*', help='The number of the column in each file that holds the readcounts. (starts at 0, will be 6 if empty)')
parser.add_argument('-platform', default='platform', help='The name of the platform.')
parser.add_argument('-study', default='study', help='The name of the study.')
parser.add_argument('-organism', default='Homo Sapiens', help='The name of the organism.')
parser.add_argument('-folder', default='./', help='The folder for the in and output files. (Optional)')
arguments = parser.parse_args()

infiles  = arguments.infiles
samples  = arguments.samples
subjects = arguments.subjects
tissues = arguments.tissues
readcountcolumn = arguments.readcountcolumn
platform = arguments.platform
study    = arguments.study
organism = arguments.organism

if infiles == None:
	print "No infiles specified"
	exit()
if samples == None:
	print "No samples specified"
	exit()
if len(infiles)!=len(samples) or len(infiles)<1:
	print "Different number of arguments or no arguments for infiles and samples"
	exit()
if subjects == None:
	subjects = samples
elif len(subjects)!=len(samples):
	print "Different number of arguments for subjects and samples"
	exit()
if tissues == None:
	tissues = []
	for sample in samples:
		tissues.append('')
elif len(tissues)!=len(samples):
	print "Different number of arguments for tissues and samples"
	exit()
if readcountcolumn == None:
	readcountcolumn = []
	for sample in samples:
		readcountcolumn.append('6')
elif len(readcountcolumn)!=len(samples):
	print "Different number of arguments for readcountcolumn and samples"
	exit()

samplescollection = {}
for sample in samples:
	samplescollection[sample] = {}

# organism = arguments.organism

platformfile = open(join(arguments.folder,platform+'-platform.txt'), 'w');
datafile = open(join(arguments.folder,study+'-data.txt'), 'w');
mappingfile = open(join(arguments.folder,study+'-subject_sample_mapping.txt'), 'w');

argumentiterator = 0
genes = []

for infile in infiles:
	infile = open(join(arguments.folder,infile),'r')
	# Remove two header rows
	infile.readline()
	infile.readline()
	for line in infile:
		words = line.strip('\n').split('\t')
		geneid = words[0]
		readcount = words[int(readcountcolumn[argumentiterator])]
		if argumentiterator == 0:
			genes.append(geneid)
		samplescollection[samples[argumentiterator]][geneid] = readcount

	argumentiterator += 1

datafile.write('PLATFORM/GPL_ID\tGENE_ID\tSAMPLE\treadcount\n')
mappingfile.write('STUDY_ID\tSITE_ID\tSUBJECT_ID\tSAMPLE_ID\tPLATFORM\tTISSUETYPE\tATTR1\tATTR2\tCATEGORY_CD\tSOURCE_CD\n')
sampleiterator = 0
for sample in samples:
	for gene in genes:
		datafile.write(platform+'\t'+gene+'\t'+sample)
		datafile.write('\t'+samplescollection[sample][gene])
		datafile.write('\n')
	mappingfile.write(study+'\t'+'\t'+subjects[sampleiterator]+'\t'+sample+'\t'+platform+'\t'+tissues[sampleiterator]+'\t'+'RNASeq'+'\t'+'\t'+'Biomarker_Data+PLATFORM+TISSUETYPE+ATTR1'+'\t'+'STD'+'\n')
	sampleiterator += 1


platformfile.write('GPL_ID\tREGION_NAME\tCHROMOSOME\tSTART_BP\tEND_BP\tNUM_PROBES\tCYTOBAND\tGENE_SYMBOL\tGENE_ID\tORGANISM\n')
for gene in genes:
	platformfile.write(platform+'\t'+gene+'\t'+'\t'+'\t'+'\t'+'\t'+'\t'+gene+'\t'+'\t'+organism+'\n')

