
# Initialize alignmentScoreGrid
def initializeAlignmentScoreGrid(seq1, seq2, gap_score):
    
    alignmentScoreGrid=[[0 for j in range(len(seq2)+1)] 
                   for i in range(len(seq1)+1)]
            
    # initialize alignmentScoreGrid for the first column (align seq1 with gaps)
    alignmentScoreGrid[0][0] = 0
    for i in range(1, len(alignmentScoreGrid)):
        alignmentScoreGrid[i][0] = alignmentScoreGrid[i-1][0] + gap_score
    for j in range(1, len(alignmentScoreGrid[0])):
        alignmentScoreGrid[0][j] = alignmentScoreGrid[0][j-1] + gap_score

    return alignmentScoreGrid            

# Use it to check whether alignmentScoreGrid is calculated correctly
def printAlignmentGrid(seq1, seq2, alignmentScoreGrid):
    
    seq1="-"+seq1
    seq2="-"+seq2
    
    print(end='\t')
    
    for j in range(0, len(alignmentScoreGrid[0])):
        print(seq2[j],end='\t')
    
    print()
    
    for i in range(0, len(alignmentScoreGrid)):        
        print(seq1[i],end='\t')    
        for j in range(0, len(alignmentScoreGrid[0])):
            print(alignmentScoreGrid[i][j], end='\t')
        print()

# Get sequence alignment values by dynamic programming
def completeAlignmentScoreGrid(seq1, seq2, alignmentScoreGrid, 
                               match_score, mismatch_score, gap_score):
    
    for i in range(1, len(alignmentScoreGrid)):
        for j in range(1, len(alignmentScoreGrid[0])):
            
            # move diagonal
            if seq1[i - 1] == seq2[j - 1]: # match
                diagonal_move = alignmentScoreGrid[i - 1][j - 1] + match_score
            else: # mismatch
                diagonal_move = alignmentScoreGrid[i - 1][j - 1] + mismatch_score

            # get score for moving down
            move_down = alignmentScoreGrid[i - 1][j] + gap_score

            # get score for moving right
            move_right = alignmentScoreGrid[i][j - 1] + gap_score
            
            alignmentScoreGrid[i][j] = max([diagonal_move, move_down, move_right])                 
            
    return alignmentScoreGrid


# Trace back the optimal alignment by getting the alignmentIndices
def traceback(seq1, seq2, alignmentScoreGrid, 
              match_score, gap_score, mismatch_score):
    
    seq1 = "-" + seq1
    seq2 = "-" + seq2    
        
    seq1_alignment=""
    seq2_alignment=""
    
    i=len(alignmentScoreGrid)-1
    j=len(alignmentScoreGrid[0])-1
    
    while i > 0 and j > 0:
        align_score = match_score if seq1[i]==seq2[j] else mismatch_score           
        
        if alignmentScoreGrid[i][j] == alignmentScoreGrid[i-1][j-1] + align_score:
            
            seq1_alignment += seq1[i]
            seq2_alignment += seq2[j]
            j = j - 1 
            i = i - 1                
            
        elif alignmentScoreGrid[i][j] == alignmentScoreGrid[i-1][j] + gap_score:
                        
            # YOUR CODE HERE
            seq1_alignment += seq1[i]
            seq2_alignment += seq2[0]  
            i = i - 1              
            
        elif alignmentScoreGrid[i][j] == alignmentScoreGrid[i][j-1] + gap_score:
            
            seq1_alignment += seq1[0]
            seq2_alignment += seq2[j] 
            j = j - 1             
            
        else:
            raise Exception("something is wrong") 
      
    seq1_alignment= seq1_alignment[::-1]
    seq2_alignment= seq2_alignment[::-1]      
            
    return (seq1_alignment, seq2_alignment)
        

# align main function
def align(seq1, seq2, match_score=2, gap_score=-1, mismatch_score=-2):
    
    alignmentScoreGrid = initializeAlignmentScoreGrid(seq1, seq2, gap_score)    
    
    alignmentScoreGrid = completeAlignmentScoreGrid(seq1, seq2, 
                                                    alignmentScoreGrid, 
                                                    match_score, 
                                                    mismatch_score, gap_score)        
    
    return (alignmentScoreGrid,
            traceback(seq1, seq2, alignmentScoreGrid,
                      match_score, gap_score, mismatch_score))
    

#seq1="GATTACAA"
#seq2="GCAT"

match_score = 2
gap_score = -1
mismatch_score = -2

printAlignmentGrid(seq1, seq2, initializeAlignmentScoreGrid(seq1, seq2, gap_score))
        
alignmentResults= align(seq1, seq2, match_score, gap_score, mismatch_score)

alignmentScoreGrid = alignmentResults[0]
alignments = alignmentResults[1]

printAlignmentGrid(seq1, seq2, alignmentScoreGrid)
print(alignments[0])
print(alignments[1])
print(alignmentScoreGrid[-1][-1])


# Compute pairwise sequence similarity from 8 homologous amino acid sequences
# the code for histone cluster 1 H1 family member a protein for 8 species
seqlist = ["MSETVPPAPAASAAPEKPLAGKKAKKPAKAAAASKKKPAGPSVSELIVQAASSSKERGGVSLAALKKALAAAGYDVEKNNSRIKLGIKSLVSKGTLVQTKGTGASGSFKLNKKASSVETKPGASKVATKTKATGASKKLKKATGASKKSVKTPKKAKKPAATRKSSKNPKKPKTVKPKKVAKSPAKAKAVKPKAAKARVTKPKTAKPKKAAPKKK", # ENST00000244573.4 human
"MSETVPPAPAASAAPEKPLAGKKAKKPAKAAAASKKKPAGPSVSELIVQAASSSKERGGVSLAALKKALAAAGYDVEKNNSRIKLGIKSLVSKGTLVQTKGTGASGSFKLNKKASSVETKPGASKVATKTKATGASKKPKKATGASKKSVKTPKKAKKPAATRKSSKNPKKPKIVKPKKVAKSPAKAKAVKPKAAKAKVTKPKTAKPKKAAPKKK", # Chimp ENSPTRT00000032884.3
"MSETVPTAPAASAAPEKPLAGKKAKKPAKAVVASKKKPAGPSVSELIVQAASSSKERGGVSLAALKKALAVAGYDVEKNNSRIKLGIKSLVSKGTLVQTKGTGASGSFKLNKKAFSVETKPGASKVAAKTKATGASKKLKKATGASKKSVKTPKKAKKPAATRKSSKNPKKPKTLKPKKVAKSPAKAKAVKPKAAKAKVTKPKTAKPKKAAPKKK", # Orangutan ENSPPYT00000018952.1
"MSETAPVAQAASTATEKPAAAKKTKKPAKAAAPRKKPAGPSVSELIVQAVSSSKERSGVSLAALKKSLAAAGYDVEKNNSRIKLGLKSLVNKGTLVQTKGTGAAGSFKLNKKAESKAITTKVSVKAKASGAAKKPKKTAGAAAKKTVKTPKKPKKPAVSKKTSKSPKKPKVVKAKKVAKSPAKAKAVKPKASKAKVTKPKTPAKPKKAAPKKK", # mouse ENSMUST00000055770.3
"MSETAPVPQPASVAPEKPAATKKTRKPAKAAVPRKKPAGPSVSELIVQAVSSSKERSGVSLAALKKSLAAAGYDVEKNNSRIKLGLKSLVNKGTLVQTKGTGAAGSFKLNKKAESKASTTKVTVKAKASGAAKKPKKTAGAAAKKTVKTPKKPKKPAVSKKTSSKSPKKPKVVKAKKVAKSPAKAKAVKPKAAKVKVTKPKTPAKPKKAAPKKK", # rat ENSRNOT00000023054.6 
"MSETAPPASATSTPPEKPAAGKKAKRPAKAAAAAKKKPTGPSVSELIVQAVSSSKERSGVSLAALKKALAAAGYDVEKNNSRIKLGLKSLVSKGTLVQTKGTGASGSFKLNKKAASGEVKANPTKVVKAKVTGTSKKPKKVTAAVKKAVKTPKKAKKPAVTKKSSKSPKKPKVVKPKKVAKSPAKAKAVKPKAAKAKVTKPKTAAKPKKAAPKKK", # Panda ENSAMET00000021358.1
"MSETAPPVPAASTPPEKPSAGRKAKKPAKAVATAKKKPAGPSVSELIVQAVSSSKERSGVSLAALKKALAAAGYDVEKNNSRIKLGLRSLVSKGTLVQTKGTGASGSFKFNKKVASVDSKPSATKVAAKAKVTSSSKKPKKATGAAAGKKGVKTPKNAKKPAATKKSSKSPKKSRVVKPKKIGKSPAKAKAVKPKAAKAKVTKPKTAAKPKKAAPKKK", # Dolphin ENSTTRT00000016728.1
"RSLTSEPSPGKSWDISGAPAKAAKKKTTASKPKKVGPSVGELIVKAVAASKDRSGVSTATLKKALAAGGYDVDKNKACVKTAIKSLVAKGSLVQTKGTGASGSFKMNKKAKKPTKKAAPKAKKPAAAKAKKPATAAKKPKKAAAAKKPTAAKKSPKKAKKAKKPAAAVAKKATKSPKKAAAKSPKKVIKKAPAAKKAPTKKAAKPKAKKAATAAKKKKSPKHK" # Tilapia ENSONIT00000015688.1
]

species = ("human", "chimp", "orangutan", "mouse", "rat", "panda", "dolphin", "tilapia")

def similarityMatrix(seqlist):
    
    sequenceSimilarity=[[0 for i in range(len(seqlist))] 
                   for j in range(len(seqlist))]
    
    sequenceSimilarity= []
    for species in range(0,len(seqlist)):
        SpeciesList = []
        seq1 = seqlist[species]
        for species2 in range(0,len(seqlist)):
            seq2 = seqlist[species2]
            alignmentResults= align(seq1, seq2, match_score=2, gap_score=-1, mismatch_score=-2)            
            alignmentScoreGrid = alignmentResults[0]             
            SpeciesList.append(alignmentScoreGrid[-1][-1])
        sequenceSimilarity.append(SpeciesList)
        
    return sequenceSimilarity

from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import numpy as np
simmat = similarityMatrix(seqlist)
sequenceSim = np.array(simmat)
dn = hierarchy.dendrogram(hierarchy.linkage(1/sequenceSim, 'single'),
                          labels=species)

plt.show() # remove comment to visualize the species dendrogram cluster

# Get consensus sequence based on pairwise similarity
def findConsensusSequence(seqlist_new):
    
    if len(seqlist_new) == 1: 
        return seqlist_new[0] #When only the final consensus seq is left in seqlist_new
    
    aligned_consensus = ""
     
    SearchSequence = similarityMatrix(seqlist_new)
    
    maxScore = -200 
    maxColumn = 0 #corresponds to the seq of most similar species 1 
    maxRow = 0 #corresponds to the seq of most similar species 2 
    for i in range(0, len(seqlist_new)):
        for j in range(0, len(seqlist_new)):
            if SearchSequence[i][j] >maxScore and j != i:
                maxScore = SearchSequence[i][j]
                maxColumn = j
                maxRow = i
    
    alignmentResults = align(seqlist_new[maxColumn], seqlist_new[maxRow], match_score=2, gap_score=-1, mismatch_score=-2)
    alignments = alignmentResults[1] #this is the returned seq_alignments 
    
    seq1Aligned = alignments[0]
    seq2Aligned = alignments[1]
    
    
    for nuc in range(0, max(len(seq1Aligned), len(seq2Aligned))):
        if seq1Aligned[nuc] == seq2Aligned[nuc]:
            aligned_consensus += seq1Aligned[nuc]
        else:
            aligned_consensus += "X"
    
    del seqlist_new[maxColumn]
    del seqlist_new[maxRow]
    seqlist_new.insert(1,aligned_consensus) #insert the new consensus sequence
    
    return findConsensusSequence(seqlist_new)

seqlist_new = seqlist[0:len(seqlist)-1] # exclude Tilapia sequence
aligned_consensus = findConsensusSequence(seqlist_new)
        
msa = [] # multiple sequence alignments

print("aligned_consensus")
print(aligned_consensus)

for i in range(0,len(seqlist)-1): # exclude tilapia    
    alignResults = align(seqlist[i], aligned_consensus)[1]    
    msa.append(alignResults[0])

print()
print("Multiple sequence alignment")
for i in range(0, len(msa)):    
    print(species[i])
    print(msa[i])
print()

# Calculate conservion score in the human sequence 
# relative to the other 6 species
human_seq_aligned = msa[0]
human_seq = seqlist[0]

conservedCounts = []

for aaPos in range(0,len(human_seq_aligned)):
    human_aa = human_seq_aligned[aaPos]
    conservedCount = 0
    if human_aa != "-":    
        for otherSeq in msa[1:(len(msa)+1)]:
            if aaPos < len(otherSeq) and human_aa == otherSeq[aaPos]:
                conservedCount += 1        
        conservedCounts.append(conservedCount)

print(conservedCounts)

consPos = 0
for aaPos in range(0,len(human_seq)):
    print(human_seq[aaPos],end='')
    if (aaPos+1) % 50 == 0:        
        print()
        while consPos <= aaPos:
            print(conservedCounts[consPos],end='')
            consPos +=1
        print()
print()        
while consPos <= aaPos:
    print(conservedCounts[consPos],end='')
    consPos +=1

