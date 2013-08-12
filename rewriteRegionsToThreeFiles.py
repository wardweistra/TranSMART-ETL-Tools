infile = open('regions_maxloss0.01.tsv','r')
regiondefinitionfile = open('GPL4091_region_platform.txt', 'w');
subjectmappingfile = open('TCGAOV_subjectmapping.txt', 'w');
samplesfile = open('TCGAOV_samples.txt', 'w');

subjects = []

# Write header for samplesfile and collect subjects for subjectmappingfile
firstlinewords = infile.readline().strip('\n').split('\t')
samplesfile.write('region_id')

for word in firstlinewords:
	if word not in ['chromosome','start','end','num.probes','loss.freq','gain.freq','amp.freq']:
		parts = word.split('.')
		subject = parts[1]+'-'+parts[2]+'-'+parts[3]
		samplesfile.write('\t'+subject+'.'+parts[0])
		if subject not in subjects:
			subjects.append(subject)

# Write subjectmappingfile
subjectmappingfile.write('STUDY_ID\tSITE_ID\tSUBJECT_ID\tSAMPLE_ID\tPLATFORM\tTISSUETYPE\tATTR1\tATTR2\tCATEGORY_CD\tSOURCE_CD')
for subject in subjects:
	subjectmappingfile.write('\nTCGAOV\t2\t'+subject+'\t'+subject+'\tGPL4091\tOvary\t\t\tBiomarker_Data+Chrom+PLATFORM+TISSUETYPE\tSTD')
	# Do we need another tab after this like in the gene expression?
	# What is SITE_ID = 2?

# Write header for regiondefinitionfile
regiondefinitionfile.write('GPL_ID\tREGION_NAME\tCHROMOSOME\tSTART_BP\tEND_BP\tNUM_PROBES\tCYTOBAND\tGENE_SYMBOL\tGENI_ID\tORGANISM')

# For ever line in infile make a line in the regiondefinitionfile and the samples file
for line in infile:
	words = line.strip('\n').split('\t')
	# Get regions name
	chromosome = words[1]
	start = words[2]
	end = words[3]
	numprobes = words[4]
	regionname = 'chr'+chromosome+':'+start+'-'+end
	# Write the regions name and values
	samplesfile.write('\n'+regionname)
	for word in words[8:]:
		samplesfile.write('\t'+word)
	# Write region definition
	regiondefinitionfile.write('\nGPL4091\t'+regionname+'\t'+chromosome+'\t'+start+'\t'+end+'\t'+numprobes+'\t\t\t\tHomo Sapiens')