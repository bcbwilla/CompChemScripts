#! /usr/local/bin/python
#
#
#
#   Doesn't work.
#
#
#
#



import subprocess
import sys

print "\n\n\n\nThis doesn't work don't use it\n\n\n\n"


if len(sys.argv) < 2:
    print "Please include two files to compare"

for i in range(1,3):
    fname = sys.argv[i]
    outf = open(fname+"JF","w")
    f = open(fname,"r")

    append = False
    for line in f:
        if "VNN" in line:
            append = True
        elif "Leave Link  701" in line:
            append = False

        if append:
            outf.write(line)
    f.close()
    outf.close()

#print subprocess.check_output(['diff', 'ftmp12345ab1', 'ftmp12345ab2'])

#subprocess.call("rm -f ftmp12345ab1")
#subprocess.call("rm -f ftmp12345ab2")


