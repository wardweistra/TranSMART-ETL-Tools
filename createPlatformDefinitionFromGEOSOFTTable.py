gpl_id = 'GPL6244'
organism = 'Homo Sapiens'

infile = open('GPL6244.annot','r')
outfile = open(gpl_id+'-platform.txt', 'w');

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
