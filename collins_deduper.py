import util
import argparse 
import re

parser = argparse.ArgumentParser(description='Software to remove PCR duplicates from RNA seq data.')
parser.add_argument('-f', help='absolute file path for sequencing data. File must be a SAM file.')
parser.add_argument('-u', help='absolute file path for list of Umis')

def createUmiDictionary(umiFile):
    """ A function that parses a file of unique UMI names and 
    returns a dicitonary where each key is an UMI from the file and
    the value is an empty Queue """
    umiDictionary = {}
    with open(umiFile) as file:
        for line in file:
            umiDictionary[line.rstrip()] = util.Queue()
    return umiDictionary

def softClipping(cigarString, strand):
    """ A function that calculates the amount of softclipping 
    present in a read and returns an offset value to adjust position."""
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
    umi = re.search("(?!.*:).*" ,qname)
    return umi.group()

def determineStrand(bitwise:int,position:int):
    if bitwise & (1 << position):
        return 'Reverse'
    return 'Forward'

def extractReadInfo(sam_line):
    components = sam_line.split()
    position =  components[1]
    strand = components[1]
    cigar_string = components[1]
    chromosome_name = components[1]

def main():
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
                sam_fields = line.split("\t")
                read_umi = extractUmi(sam_fields[0])
                chromosome = sam_fields[2]
                bitwise = sam_fields[1]
                position = sam_fields[3]
                cigar_string = sam_fields[5]
                strand = determineStrand(int(bitwise),4)
                offset = softClipping(cigar_string, strand)
                fixed_position = int(position) - int(offset)

                # chromosome, position, strand 
                key_value = f'{chromosome}_{strand}_{fixed_position}'
                if read_umi in umi.keys():
                    if umi[read_umi].itemNotInQueue(key_value):
                        output_file.write(line)
                    umi[read_umi].push(key_value)
                    umi[read_umi].lengthLimit()
    output_file.close()

main()