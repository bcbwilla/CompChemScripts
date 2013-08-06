#
#  This script calculates the distance between a graphene
#   nanoribbon surface and adsorbed target atom.
#
#  It pulls all of the needed angle and distance data
#   from a Gaussian .log file and computes the distance
#   as an average of the distances from surrounding 
#   carbon atoms.
#
#  The script takes command line agruments:
#  - the name of the Gaussian log file
#  - the atom number* of the target (adsorbed) atom
#  - the atom numbers (space separated) of all of the nearest 
#     ring atoms (for distance determination)
#  - the atom numbers of all of the next-nearest ring atoms
#     (for angle determination)
#
#  For Lithium adsorbed on graphene nanoribbons, this means you 
#   should be including 13 total atoms
#
#
# *The atom number is NOT the atomic number, but the unique 
#   number that Gaussian assigns to each atom to keep track 
#   of it.
#
#  Ben Williams, Aug 6, 2013
#
#

import math
import sys

#
# INPUT SECTION
#

if len(sys.argv) < 15:
    print "Enter log file name and 13 atom numbers"

filename = sys.argv[1]
target = sys.argv[2] # adsorbed metal atom

# list of inner ring atoms
inner_ring = []
for i in range(3,9):
    inner_ring.append(sys.argv[i])
# list of next nearest ring atoms
outer_ring = []
for i in range(9,15):
    outer_ring.append(sys.argv[i])

print "Filename: %s" % filename
print "Target atom: %s" % target
print "Inner ring: %s" % inner_ring
print "Outer ring: %s" % outer_ring
print "Total atoms: %d" % (len(outer_ring) + len(inner_ring) + 1)

#
# FILE PROCESSING SECTION
#

# this set is for comparison puproses to link together angles and distances
all_atoms = set([target] + inner_ring + outer_ring)
distance_data = []   # where all the info is dumped for later analysis
angle_data = []      #
correct_section = False  # true when in the part of log file with dist/ang data


f = open(filename)
for line in f:
    # check if in correct section of file
    if " ! Name  Definition              Value          Derivative Info." in line:
        correct_section = True
        next(f)
    elif "-------------------------------------------" in line:
        correct_section = False

    if correct_section:
        l = line.split() # split into bits to analyze
        # check if target atom is in line
        if len(l) == 8 and target in l[2]: 
            atoms = l[2][2:-1].split(",")
            if 'A' in l[1] and atoms[-1] == target and set(atoms) <= all_atoms:
                angle = 180 - float(l[3])
                angle_data.append((atoms,angle))
                
            elif 'R' in l[1] and set(atoms) <= all_atoms:
                distance = float(l[3])
                distance_data.append((atoms,distance))
f.close()

#
# ANALYSIS SECTION
#

if len(distance_data) != len(angle_data) or len(distance_data) != 6:
    print "\n\n!!! Could not find all of the data !!! \n\n"

print "\nPairing angle with distance for computation."
print "Angle Atoms          Dist. Atoms  Angle Dist. Height"
h_total = 0
for dist in distance_data:
    for ang in angle_data:
        # pair up the angles and distances
        if dist[0][0] in ang[0]: # the angle and distance go together
            ai = ang[1]
            di = dist[1]
            hi = di*math.sin(math.radians(ai))
            h_total += hi
            print "%s  %s  %.2f  %.2f  %.4f" % (ang[0], dist[0], ai, di, hi)
        

h_avg = h_total / 6.0

print '\nAverage height:'
print h_avg


