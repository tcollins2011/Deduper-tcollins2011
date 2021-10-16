# Define the Problem

    As a result of PCR being a necessary step in next-generation sequencing techniques, PCR duplicates are introduced into sequencing data. These duplicates have the potential to confound downstream analysis and can lead to inaccurate genome assemblies. As a result, these duplicates need to be removed from our sequencing data. However, there are some potential pitfalls when attempting to do this. First and foremost it can be difficult to recognize a PCR duplicate vs a normal highly expressed read  Additionally, depending on when we try to do this in our RNA workflow, the computational time can vary drastically and our approach might need to fundamentally change. In our case, we will be attempting to solve this problem post-alignment in order to reduce the computational complexity and will be deploying several strategies to sucessfully identify true PCR duplciates. 
    
    To identify and remove PCR duplicates we will be focusing on several key factors. First a PCR duplicate by necessity must have the same start site as another read, be positioned on the same chromsome, and be located on the same strand of DNA. These basic requirements will allow us to determine if two pieces of DNA are actually identically placed in the genome. However, this doesn't fully remove the possibility that these could be two legitimate reads that by chance matched up perfectly. So in UMI's were added to each DNA read in the wet lab before PCR to add unique DNA patterns on either side of read. If these UMI's are the same and all the before mentioned considerations are met we can be confident in declaring a read a PCR duplicate. Additonally, there is a final confounding factor: soft clipping. Soft clipping arises as a result of the imperfect nature of DNA replication and the sequencing prcoess and can cause some reads to report a start position that is slightly off there true location, due to the first nucleotides of the sequence being ignored. This additional problem will need to be adressed as well through a clipping algorithm below.


# Overall Generic Algorithm

    Create a dictionary where every key is a value from an UMI file
    Intialize a queue for each of these keys to store data
    Sort a Sam file by position 
    Read through every line in a SAM file
    For every line extract a string containing its corrected_position,strandness, and chromosome name
    For every line extract its UMI
    Check to see if Umi in Dictionary
    If Umi in Dictionary check queue to see if extracted string is in it
    If no match add string to queue, check queue length to determine if entries should be popped and write the line to the output file
    End once every line sam File has been read in
    

# Testing

<!-- These are initial test ideas. More will be added and flushed out while the prroject is actually coded. -->

    Testing files have been uplaoded to github and will be named to match the function that they apply to. 

    UMI_dictionary_test.txt - a file that contains 4 UMI's and can be run to determine to test the UMI_Dictionary function

    soft_clipping_test.sam = a sam file with a variety of soft clipping changes present to test the soft_clipping function

    duplicate_test.sam - a sam file that has 2 duplicate lines to test the algorithms abbility to filter our duplicates 

    test.sam - a provided sam file that simulats a small set of data for general purpose data

<!-- Ideally a couple full testing suites will be written with the actual code to prove its working the way it should -->

# Pseudo Code Algorithm

<!-- Code to create a Queue Data structure -->

class Queue:

``` Simple Queue class setup```
    
    <!-- Initialization Function -->
    def __init__(self) 
        self.list = []
        end

    function push(self,item) *return* inserts item in position 0 of queue
        self.list.insert(0,item)
        end

    function pop(self) *return* last item of Queue
        return self.list.pop()
        end

end

 
<!-- Initalize Dictionary of UMI's from reading in the UMI file provided  -->

function UMI-Dictionary(UMI_file) *return* a dictionary 
    
``` Initalizes a dictionary where every UMI value from a provided file is a key```


    working_dict <- an empty dictionary
    working_file <- open(UMI_file, 'r')

    for line in working_file do 
        working_dict[line] = queue()
    
end 


<!-- Correct for soft Clipping -->

function Soft_Clipping(cigar string) *return* position_offset

``` This function corrects for soft clipping by searching the cigar string for any S and returnign the number that comes before it ```

    import re

    position_offset <- 0

    if cigar string matches ('S') then
        position_offset = number perceeding S
   
end

<!-- Identify Read -->

function Extract_read_Info(sam_line) *return* string

``` This function creates a string that contains the chromsome name, corrected starting postion, and strandedness of a line from the sam file```
    
    components <- split sam_line by spaces
   
    destructure position, strand, cigar_string, chromosome_name from components

    correction <- Soft_Clipping(cigar_string)

    position <- position - correction
    unique_identfier <- chromosome_name + strand + position 


end

<!-- Extract UMI from Sam Read -->

function Extract_Umi(sam_line) *return* string


``` Extracts the Umi from the QNAME of a Sam File```

    import re
    target <- index[0] of  split(sam_line)
    Extract Umi from QNAME

end


<!-- Main Function -->

function Main(UMI_File, SAM_File) *return* a deduplexed sam file

``` Main functional loop to create a deduplexed file. Calls all other functions and provides overall workflow.```

    working_dict <- UMI-Dictionary(UMI_File)
    output <- write_file

    loop do 
        if SAM_File empty *then* *return* file
        umi <- Extract_Umi(sam_line)
        read <- Extract_read(sam_line)

        if umi in working_dict.keys()  *then*
            if read in working_dict[umi] *then*
                pass
            
            add read to working_dict[umi]

            if len(working_dict[umi]) > some number
                pop working_dict[umi]
    end

end 

# Output

Two files showing the input and output have been added as well. These files are currently just generic sam files that include all elements that would are required for this file type. Additional header information may be present in either file, however at this stage what would go in the header has not been decided yet. Depending on the input files, an additional chekc will most likely need to be made in the code to ensure it only runs on actual data entry lines. 

Additionally, we would expect the output file to be smaller than the input file and to contain no duplicates, but still maintain the same format.

