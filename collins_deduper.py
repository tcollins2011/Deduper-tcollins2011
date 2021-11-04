import argparse 
import re

parser = argparse.ArgumentParser(description='Software to remove PCR duplicates from RNA seq data.')
parser.add_argument('-f', help='absolute file path for sequencing data. File must be a SAM file.')
parser.add_argument('-u', help='absolute file path for list of Umis')

def createUmiDictionary(umiFile):
    """ A function that parses a file of unique UMI names and 
    returns a dicitonary where each key is an UMI from the file and
    the value is an empty set """
    umiDictionary = {}
    with open(umiFile) as file:
        for line in file:
            umiDictionary[line.rstrip()] = set()
    return umiDictionary

def softClipping(cigarString, strand):
    """ A function that calculates the amount of softclipping 
    present in a read and returns an offset value to adjust the reads 
    start position."""
    positionOffset = 0

    # Forward Strand Logic
    if strand == 'Forward':
        if 'S' in cigarString[0:3]:
            softclip = re.search("^[^S]*",cigarString)
            positionOffset = -1 * int(softclip.group())

    # Reverse Strand Logic
    else:
        # Calculate off set to add
        for i in (re.findall(r'\d+', cigarString)):
            positionOffset += int(i)
        # Remove any deletions from offset
        for i in (re.findall(r'(\d*)D', cigarString)):
            positionOffset -= int(i)
        # Remove 5' softclip
        for i in (re.findall(r'(\d*)S$', cigarString)):
            positionOffset -= int(i)


    return positionOffset

def extractUmi(qname):
    """ A function that extracts an UMI identifier from a qname"""
    umi = re.search("(?!.*:).*" ,qname)
    return umi.group()

def determineStrand(bitwise:int,position:int):
    """ A function that determines if a specific bit is 1 or 0. This determines
    if a strand is forward or reverse"""
    if bitwise & (1 << position):
        return 'Reverse'
    return 'Forward'

def extractReadInfo(sam_line):
    """ A function that extracts relevant information from a SAM file and calls helper functions"""
    sam_fields = sam_line.split("\t")
    read_umi = extractUmi(sam_fields[0])
    chromosome = sam_fields[2]
    bitwise = sam_fields[1]
    position = sam_fields[3]
    cigar_string = sam_fields[5]

    strand = determineStrand(int(bitwise),4)
    offset = softClipping(cigar_string, strand)
    fixed_position = int(position) - int(offset)

    return read_umi, chromosome, strand, fixed_position

def main():
    """ Main Loop. This function takes in a sam file and umi List and removes PCR duplicates from the sam file"""
    args = parser.parse_args()
    sam_file = args.f
    umi_file = args.u

    umi = createUmiDictionary(umi_file)

    output_file = open(f'deduped_sam_file', "w")

    with open(sam_file) as sf:
        for line in sf:
            if line.startswith('@'):
                output_file.write(line)
            else:
                read_umi, chromosome, strand, position = extractReadInfo(line)
                key_value = f'{chromosome}_{strand}_{position}'
                if read_umi in umi.keys():
                    if key_value not in umi[read_umi]:
                        umi[read_umi].add(key_value)
                        output_file.write(line)
    output_file.close()

main()