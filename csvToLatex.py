""" This short script converts a CSV table into latex table.
    
    This ideally works with a large CSV table, because it is 
    a pain to manually type them into latex. It has minimal 
    configuration options.  The idea is to do 90% of the work
    with this script, leaving only small manual tweaks after.


    Command Line Arguments:

    required positional arguments:
      infile                input file name

    optional arguments:
      -h, --help            show this help message and exit
      -ncols N, --numbercolumns N
                            number of columns in file
      -vd, --verticaldivider
                            adds vertical dividers to table
      -hd, --horizontaldivider
                            adds horizontal dividers to table
"""

import csv
import sys
import argparse

# define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument("infile", help="input file name")
parser.add_argument("-ncols", "--numbercolumns", type=int, help="number of columns in file", default=2)
parser.add_argument("-vd", "--verticaldivider", action="store_true", help="adds vertical dividers to table")
parser.add_argument("-hd", "--horizontaldivider", action="store_true", help="adds horizontal dividers to table")
args = parser.parse_args()

# csv input and latex table output files
infile = args.infile
outfile = infile +".table"

with open(infile, 'r') as inf:
    with open(outfile, 'w') as out:
        reader = csv.reader(inf)
        
        # build the table beginning code based on number of columns and args
        # columns all left justified
        code_header = "\\begin{tabular}{"
        for i in range(args.numbercolumns):
            code_header += " l "
            if i < args.numbercolumns - 1 and args.verticaldivider:
                code_header += "|"
        code_header += "}\n\\hline\n"
        out.write(code_header)
        
        # begin writing data
        for row in reader:
            # replace "," with "&"
            if args.horizontaldivider:
                out.write(" & ".join(row) + " \\\\ \\hline\n")
            else:
                out.write(" & ".join(row) + " \\\\ \n")
        
        if not args.horizontaldivider:
            out.write("\\hline\n")

        out.write("\\end{tabular}")

