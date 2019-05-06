mRNA = input("Enter a mRNA sequence: ")
miRNA = input("Enter a microRNA sequence: ")

complement = "" # same begining as microRNA code

for nuc in miRNA[1:7]:
    if nuc == "A":
        complement = complement + "U"
    if nuc == "U":
        complement = complement + "A"
    if nuc == "C":
        complement = complement + "G"
    if nuc == "G":
        complement = complement + "C"

miRNArev = complement[::-1] 

index = 0
occurence=0
NucPositionList = [] 
    
while index <= len(mRNA)-6:    
    
    if mRNA[index:index+6] == miRNArev:
        occurence = occurence + 1
        nucPositionString = "microRNA seed match is found at mRNA sequence position " + str(index) 
        NucPositionList.append(nucPositionString) #appending the positions in the mRNA where a basepairing is found 
    index = index + 1

print("The mRNA has", occurence, "target site(s)")

for nuc in NucPositionList: #Loop so that each nucleotide position in the list can be printed 
    print(nuc)
