$infile = $ARGV[0];
$outfile = "G03-".$infile;
$find = "Atom  AN";
$replace = "Atom AN";
      
open INFILE,"<$infile" or die "Cannot read the file $infile: $!\n";
open (OUTFILE, ">$outfile") || die ("Could not open $outfile; $OS_ERROR");

while ($line = <INFILE>)
{
    $line =~ s/$find/$replace/;
    print OUTFILE $line;
}

close(FILE);
close(OUTFILE);

