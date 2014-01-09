#!/usr/bin/env groovy
@Grab(group='net.sf.opencsv', module='opencsv', version='2.3')

import au.com.bytecode.opencsv.CSVReader

def pathToSampleFile = args[0]
def columnsCustomOrder = ['.chip', '.segmented', '.flag', '.probloss', '.probnorm', '.probgain', '.probamp']
def regionColumnName = 'region_id'
def separator = '\t'

def doWithRows = { closure ->
	def tsvReader = new CSVReader(new BufferedReader(new FileReader(pathToSampleFile)), (char) separator)
	try {
		String[] header
		header = tsvReader.readNext()
		if(header) {
			String[] row
			int rowNumber = 0
			while ((row = tsvReader.readNext()) != null) {
				def rowMap = (0..header.length - 1).collectEntries { indx -> [(header[indx]) : row[indx]]	}
				if(!closure(++rowNumber,rowMap)) {
					break;
				}
			}
		}
	} finally {
		tsvReader.close()
	}	
}

showUnmapped = false

doWithRows { rowNumber, rowMap ->
	def regionColumnMap = rowMap.find { it.key == regionColumnName }
	def sampleGroups = [] as LinkedHashSet
	def columnNames = rowMap.keySet()
	def unmappedColumnNames = []
	columnNames.each { columnName ->
		def suffix = columnsCustomOrder.find { columnName.endsWith(it) }
		if (suffix) {
			sampleGroups << columnName.replace(suffix, '')
		} else {
			unmappedColumnNames << columnName
		}
	}
	if(showUnmapped) print "unmapped = $unmappedColumnNames"
	if(rowNumber == 1) {
		print "${regionColumnMap.key}$separator"
		sampleGroups.each { sampleGroup ->
			columnsCustomOrder.each { suffix ->
				print "${sampleGroup}${suffix}$separator"
			}
		}
		print '\n'
	}
	print "${regionColumnMap.value}$separator"
	sampleGroups.each { sampleGroup ->
		columnsCustomOrder.each { suffix ->
			print "${rowMap[sampleGroup + suffix]}$separator"
		}
	}
	print '\n'
	return true
}