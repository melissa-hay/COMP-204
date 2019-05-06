mRNA = input("Enter a mRNA sequence: ")
miRNA = input("Enter a microRNA sequence: ")

complement = "" 

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
while index <= len(mRNA)-6:    
    
    if mRNA[index:index+6] == miRNArev: #searching for the occurence of miRNArev in the long mRNA sequence
        occurence = occurence + 1
    
    index = index + 1

print("The mRNA has", occurence, "target site(s)")

