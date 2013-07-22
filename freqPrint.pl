# This script copys the the frequency data from a .log Gaussian
#  file and then copies it to a .csv file with a "freq_" prefix
#
use English;

@freqAr; #array for storing frequency data
@irAr;	#array for storing IR intensity data
$infile; #input file name, for use with chop()

# read each input file from the command line
while (<>) {
# if the line has the keyword, store the line in a matrix
	if ($ARG =~ "Frequencies") {
		push(@freqAr, $_);		
	}

	if ($ARG =~ "IR Inten") {
		push(@irAr, $_);		
	}

}

#chops the input file name to get rid of .log extension
$infile = $ARGV;
chop($infile);
chop($infile);
chop($infile);

#define output file name based on input file name
$outfile = "freq_".$infile."csv";

# open a file to store the results
open (OUTPUT, ">$outfile") || die ("Could not open file results.txt; $OS_ERROR");

#print heading
print "#Frequency,IR Int\n";
print OUTPUT "#Frequency,IR Int\n";

# define array size for for loop
$arraySize = $#irAr + 1;

# use "substr" to pick out the data from each line in the array, and print
# it to both the terminal and output file.
 for ($i = 0; $i < $arraySize; $i++) {
 	print OUTPUT substr($freqAr[$i], 16, 10).",".substr($irAr[$i], 16, 10)."\n";
	print OUTPUT substr($freqAr[$i], 39, 10).",".substr($irAr[$i], 39, 10)."\n";
	print OUTPUT substr($freqAr[$i], 62, 10).",".substr($irAr[$i], 62, 10)."\n";

 	print substr($freqAr[$i], 16, 10).",".substr($irAr[$i], 16, 10)."\n";
	print substr($freqAr[$i], 39, 10).",".substr($irAr[$i], 39, 10)."\n";
	print substr($freqAr[$i], 62, 10).",".substr($irAr[$i], 62, 10)."\n";
	 } 


# close the output file
close (OUTPUT);

