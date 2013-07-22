#! /usr/bin/python

import sys

"""
Computes counterpoise correction
"""

if len(sys.argv) != 2:
    print "oops"

energy = []
# remove extra stuff 
for line in open(sys.argv[1]).readlines():
    energy.append(float(line.rstrip()[22:43]))
    print float(line.rstrip()[22:43])

print "CP Correction: ",energy[0] + energy[1] - energy[2] - energy[3],"hartrees"
