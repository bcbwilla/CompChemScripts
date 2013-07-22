#! /usr/bin/python
import sys

"""
This program generates necessary ghosted geometry files for use in calculating the
BSSE error.  For use with two fragments: one being metal atom and the other being 
graphene.

Command line inputs:
1 file containing geometry data (no spin of multiplicity line!)
2 name of file, used as base for writing new files
3 name of metal atom ("He, Ne, ..." etc)
4 atomic number of metal atom

"""

key_string = " Number     Number "


if len(sys.argv) != 5:
    print "oops"
geom = sys.argv[1]          #read geom date from file
filename = sys.argv[2]      #read name of file
atom_name = sys.argv[3]     #read name of atom
atom = sys.argv[4]          #read atom number

if filename.endswith('.geom'):
    filename=filename[:-5]

f = open(geom).readlines()
coordinates_temp=[] #temp array

# remove extra stuff 
for line in f:
    coordinates_temp.append(line.rstrip()[15:25]+line.rstrip()[30:]) 

# replace atom number by atom symbol
coordinates=[]
for line in coordinates_temp:
    if atom in line[:4]:
        coordinates.append(line.replace(atom, atom_name,1))
    elif ' 1 ' in line[:4]:
        coordinates.append(line.replace(' 1 ','H ',1))
    elif ' 6 ' in line[:4]:
        coordinates.append(line.replace(' 6 ','C ',1))
    elif '-2' in line[:4]:
        coordinates.append(line.replace('-2 ','Tv',1))

#Ghost metal case
out_file = open(filename+"-"+atom_name+"G.geom","w")

for line in coordinates:
    if atom_name in line[:4]:
        out_file.write(line.replace(atom_name+'   ', atom_name+'-bq',1)+"\n")
    else:
        out_file.write(line+"\n")

out_file.close()
print "Written ghost "+atom_name+" case to "+ filename+"-"+atom_name+"G.geom"

#Ghost graphene case
out_file = open(filename+"-rG.geom","w")

for line in coordinates:
    if ' H ' in line[:4]:
        out_file.write(line.replace(' H   ',' H-bq',1)+"\n")
    elif ' C ' in line[:4]:
        out_file.write(line.replace(' C   ',' C-bq',1)+"\n")

    else:
        out_file.write(line+"\n")

out_file.close()
print "Written ghost graphene case to "+ filename+"-rG.geom"


#No metal case
out_file = open(filename+"-No"+atom_name+".geom","w")

for line in coordinates:
    if atom_name in line[:4]:
        pass
    else:
        out_file.write(line+"\n")

out_file.close()
print "Written no "+atom_name+" case to "+ filename+"-No"+atom_name+".geom"


#No graphene case
out_file = open(filename+"-NoGr.geom","w")

for line in coordinates:
    if ' H ' in line[:4]:
        pass
    elif ' C ' in line[:4]:
        pass
    else:
        out_file.write(line+"\n")

out_file.close()
print "Written no graphene case to "+ filename+"-NoGr.geom"


