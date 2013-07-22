#! /usr/bin/python

import sys


'''Script for handling partial density of states
'''

####    ####    ####    ####    ####    ####    ####    ####

'''Enter atoms and orbitals of interest in this dictionary!'''

in_dictionary = {'C':['2S','2PX','2PY','2PZ','3PX','3PY','3PZ'],'S':['3S','3PX','3PY','3PZ','4S','4PY','4PZ'], \
		 'H':['1S','2S'], 'N':['2S','2PX','2PY','2PZ','3S','3PX','3PY','3PZ']}

####    ####    ####    ####    ####    ####    ####    ####



start_string = 'Gross orbital populations:'
end_string = 'Condensed'

if len(sys.argv) == 2:
	try:
		filename = sys.argv[1] 			#read filename from command line
	except IOError:
		sys.exit('File not found!  Try harder.')
else:
	sys.exit('Enter a .log filename after the program name!')


def get_raw_data(filename, start_string, end_string):
	'''This function pulls data from input file named filename starting at 
	start_string and ending at end_string.  It returns a list, and
	each entry is a line of data.
	'''

	import re
	lines = []
	infile = open(filename, 'r')
	line = infile.readline()  	#get first line
	line.rstrip()			#get rid of \n at end

	while True:
		if not line:
			break	
		line = infile.readline()
		line.rstrip()
	
		if re.search(start_string, line):
			line = infile.readline() 
			line = infile.readline() 
			while not re.search(end_string, line):
				if not line:
					print "File ended without finding"+end_string
					break			
				lines.append(line.rstrip())
				line = infile.readline() 
			
	infile.close()		
	return lines



lines = get_raw_data(filename, start_string, end_string)

def build_atom_dict(lines): 
	''' Takes a list of orbital data and returns atomic orbtial dictionary
	with format {'Atom Sym': {'Atom #': [['orbital', orbital #, Cont.],...],...},...}
	Note that 'Atom #' is NOT the atomic number, but from the numbering system Gaussian
	uses to keep track of atoms
	'''

	import re					#regex module
	atom_dict = {}					#dictionary for storing orbital info
	i = 0						#loop counter
	
	while i < len(lines):				#while not a blank line

		if re.match('\w', lines[i][9]):			#search for atomic symbol
			element_sym = lines[i][9:11].strip()	#store element symbol
			element_num = int(lines[i][5:8])	#store element number

			if element_sym not in atom_dict:
				atom_dict[element_sym] = {}	#add new elements to dict. with blank
								#dict for storing each atom
			inner_list = []
			inner_list.append([lines[i][12:17].strip(), \
					  int(lines[i][0:4]),float(lines[i][24:31])])
			i += 1
	
			while i < len(lines) and not re.match('\w', lines[i][9]):	#while not a new atom
				inner_list.append([lines[i][12:17].strip(), \
						  int(lines[i][0:4]),float(lines[i][24:31])])
			
				i += 1
			atom_dict[element_sym][element_num] = inner_list	#add orbitals to atom
		else:
			i += 1

	return atom_dict

orbital_dictionary = build_atom_dict(lines)
#print orbital_dictionary

def pull_orbitals(orb_d,in_d):
	'''Takes an orbital dictionary as built by build_atom_dict function, with dictionary structure:
	{'Atom Sym': {'Atom #': [['orbital', orbital #, Cont.],...],...},...}
	and a dictionary with element symbols as keys and a list of desired orbitals as values:
	{'Atom Sym':[orb1,orb2,...],...}
	Returns a list of orbital numbers for use in PDOS script.
	'''

	orbital_number_list = []
	
	for atom in in_d.keys():					#loop through list of desired atoms
		if atom in orb_d:					#check if atom is in orbital_dictionary
			for atom_num in orb_d[atom]:			#loop through atom num of each desired atom in orbital_dictionary
				for e in orb_d[atom][atom_num]:		#given a desired atom of certain number, search look at orbitals
					if e[0] in in_d[atom]:		#if orbital is wanted, add to orbital_number_list
						orbital_number_list.append(e[1])

	orbital_number_list.sort()
	
	orbital_string = ''
	for orbital in orbital_number_list:
		orbital_string = orbital_string + str(orbital) + ' '	
	
	orbital_string = orbital_string[:-1]

	return orbital_string



print pull_orbitals(orbital_dictionary,in_dictionary)
	


