sequence = input("Enter a DNA sequence: ")
invalidSequence = False 

for index in range (0, len(sequence)): #To scan user's sequence and determine whether or not it contains the correct letters
    letter = sequence[index]

    if letter == "A" or letter == "G" or letter == "C" or letter == "T":
        invalidSequence = False          
    else:
        print("Invalid Sequence")
        invalidSequence = True # Used to prevent a user's sequence with invalid letters from being analyzed in any subsequent loops or conditionals
        break 

index = 0
cpgDetected = False # used later on to discriminate between a user's sequence that has CpGs versus one that doesn't have CpGs

while index <= len(sequence)-2 and not invalidSequence: #To check for CpG sites in the user's sequence given it was found to contain correct letters only   
    
    if sequence[index:index+2] == "CG":
        print("CpG site is detected at position", index, "of the sequence")
        cpgDetected = True
    
    index = index + 1
    
if not cpgDetected and invalidSequence == False:  
    print("no CpG site is detected in the input sequence")


