#! /usr/local/bin/python
#
#   This is a specific analysis script for the
#    Li adsoprtion on B and N doped graphene 
#    nanoribbon project.  
#
#   It calculates the distance between Li and
#    either B or N and extracts the Mulliken 
#    atomic charges for Li, N and B atoms 
#    from a Gaussian log file.
#
#   To run, go to the directory containing the log
#    files and do
#   
#    python /casa/benw/scripts/getcharge.py
#

import os
import subprocess
from math import sqrt

# helper function to calculate distance between atoms
def distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)


print "Processing files..."

# Store all of the information from the log files as a list
# of dictionaries.  Each log file is a dictionary.
all_file_data = []
# find log files
for file in os.listdir("."):
    if file.endswith(".log"):
        # check if job completed sucessfully
        tail = subprocess.check_output(["tail",file])
        if not "Finished at" in tail:
            print str(file)+" hasn't finished running. Skipping it"
        elif "Error termination" in tail:
            print "Error termination in "+str(file)+". Skipping it"
        else:
            print "File okay. In file "+str(file)
            # lots of flags to keep track of which section of file we are in
            charges = False     # true if in charges section
            geom = False        # true if in geometry section
            li = False          # true if Li adsorbed
            p1,p2 = False,False # atomic coordinate points

            d = {}
            d['filename'] = file
            f = open(file, 'r')

            for line in f:
                # see if entering charge section of file
                if "Mulliken atomic charges" in line and "=" not in line:
                    charges = True
                elif "Mulliken charges with hydrogens summed into heavy atoms:" in line:
                    charges = False
                # see if entering coordinate section of file
                elif "Coordinates" in line:
                    geom = True
                elif " Lengths of translation vectors:" in line:
                    geom = False 
                # get charge info
                if charges:
                    if "Li" in line:
                        li = True
                        d['Li'] = line.strip().split()[2]
                    elif "B" in line or "N" in line:
                        d['other'] = line.strip().split()[2]
                # get geometry info for distances
                elif geom:
                    l = line.split()
                    if len(l) >= 2:
                        if  l[1] == "3":
                            p1 = (float(l[3]), float(l[4]), float(l[5]))
                        elif l[1] == "5" or l[1] == "7":
                            p2 = (float(l[3]), float(l[4]), float(l[5]))
                            
            if not li:
                d['Li'] = 'N/A'
            if p1 and p2:
                d['distance'] = distance(p1,p2)
            else:
                d['distance'] = "N/A"
            all_file_data.append(d)
        
        f.close()

# print the results
print 
print
print "file,Li charge,other charge,distance"
# do by functional
for d in all_file_data:
    if "HSE1PBE" in d['filename']:
        print d['filename']+","+d['Li']+","+d['other']+","+str(d['distance'])

for d in all_file_data:
    if "PBEPBE" in d['filename']:
        print d['filename']+","+d['Li']+","+d['other']+","+str(d['distance'])
print

