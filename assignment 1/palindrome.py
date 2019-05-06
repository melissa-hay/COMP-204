# Melissa Hayalioglu
# 260714271 
invalidSequence = False
sequence = input("Enter a DNA sequence: ")

complement = ""
for index in range (0, len(sequence)):
    if sequence[index] == "A":
        complement = complement + "T"
    elif sequence[index] == "G":
        complement = complement + "C"
    elif sequence[index] == "C":
        complement = complement + "G"
    elif sequence[index] == "T":
        complement = complement + "A"          
    else:
        print("Invalid Sequence")
        invalidSequence = True
        break

if not invalidSequence:
    if sequence == (complement[::-1]):
        print(sequence, "is a palindromic sequence")
    else:
        print(sequence, "is not a palindromic sequence")
    
