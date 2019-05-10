import pandas as pd
import json
import math
import re 

# reading ICD-9 definitions
def process_icd9_file(filename):
    """
    args:
        filename: Name of file containing ICD-9 definition
    returns:
        dictionary of dictionaries
        level 1 dictionary: icd9 group name as key
        level 2 dictionary: icd9 code as key and icd9 names as values
    """
    icd9_encyclopedia={}
    
    f = open(filename, 'r')

    groupName = ''
    dict2= {}
    
    while (True):
        line = f.readline().rstrip()
        #search group name
        group_name = re.search( r'^[a-zA-Z]{2,}.*', line.rstrip())  
        #search individual icd9 codes and their names
        disease = re.search( r'(^[a-zA-Z]*.*[0-9]+)(.*[a-zA-Z].*[a-zA-Z])', line.rstrip())           
        if line == "": #we've reached the end of the file
            icd9_encyclopedia[groupName] = dict2
            break
        elif group_name:
            
            if groupName !='':
                
                icd9_encyclopedia[groupName] = dict2
                
            groupName = group_name.group()
            dict2= {}
            
        else:
            icd9_code = disease.group(1)
            icd9_name = disease.group(2)
            dict2[icd9_code] = icd9_name    

    f.close()
    
    return icd9_encyclopedia

icd9_encyclopedia = process_icd9_file("icd9_info.txt")

# check
count = 0
print("\n\n**** output ****")
for k,x in icd9_encyclopedia.items():
    print('group name', k, sep='\t')
    for k1,x1 in x.items():
        print(k1, x1, sep='\t')
        count+=1
    if count > 10:
        break

# Process patient data to read in 1000 patients
def process_patient_data(filename, max_patients=5000):
    """
    args:
        filename: "DIAGNOSES_ICD.csv.gz"
        max_patients: optional argument for maximum number of patients to store
        in the dictionary
    returns:
        a dictionary with patient ID as key and a set of ICD-9 code as values
        NOTE: the ICD-9 code from DIAGNOSES_ICD.csv.gz is not directly compatible
        with the ICD9_encyclopedia from function process_icd9_file()
        This function will parse the ICD-9 code as follows:
        If the ICD-9 code is numeric or starts with "V", the first 3 characters
        of each ICD-9 code is stored as the values in the ICD-9 list; 
        If the ICD-9 code starts with "E", the first 4 characters of the ICD-9
        code is stored as the values in the ICD-9 list
    """

    patient_data = pd.read_csv(filename, compression="gzip")

    patient_data = patient_data.sort_values(by=['SUBJECT_ID'])

    patient_records = {}
    
    # To keep track each of time patID changes 
    prev_patID = 0 
    #to break out of loop when patientCount exceeds max_patients 
    patientCount = 0 
    
    for index, row in patient_data.iterrows():        
        patID = row['SUBJECT_ID'] #access column "SUBJECT_ID"
        
        icd9_code = str(row['ICD9_CODE']) #access column "ICD9_CODE"
        
        if icd9_code.startswith('E'):
            patient_records.setdefault(patID,[]).append(icd9_code[0:4])
        
        elif icd9_code.startswith('V'):
            patient_records.setdefault(patID,[]).append(icd9_code[0:3])            
        
        elif isInt(icd9_code):
            patient_records.setdefault(patID,[]).append(icd9_code[0:3])            
        
        if prev_patID != patID:
            patientCount += 1 
            prev_patID = patID           
            if patientCount > max_patients:
                break        
    
    for key, values in patient_records.items():
        patient_records[key]= (set(values))

    return patient_records

#Check numeric value 
def isInt(v):
    try:     
        intTest = int(v)
    except:
        return False
    return True         

patient_records = process_patient_data("DIAGNOSES_ICD.csv.gz")

# check
count = 0
print("\n\n**** output ****")
for k,x in patient_records.items():
    print(k, x ,sep='\t')
    count += 1
    if count > 10:
        break

def average_patient_icd9code(patient_records):
    """
    args:
        patient_records obtained from process_patient_data("DIAGNOSES_ICD.csv.gz")
    returns:
        average number of patient observed per ICD-9 code
    """
    
    Dict = {} #track the number of patients observed for each icd9 code   

    for patID, diseases in patient_records.items():
        for disease in diseases:        
            if disease in Dict:
                Dict[disease] += 1
            else:
                Dict[disease] = 1
    #Get average number of patients observed for any icd9 codes
    icd9sum = ( sum(Dict.values()) )/(len(Dict))
    
    return icd9sum


print("\n\n**** output ****")
print(f"Average patient count {average_patient_icd9code(patient_records):.2f}") # 57.53


#Group patient icd9 code by icd9 categories
def process_icd9_encyclopedia(icd9_encyclopedia):
    """
    args:
        icd9_encyclopedia obtained from process_icd9_info("icd9_info.txt")
    returns:
        icd9_encyclopedia_reverseIndex: dictionary with key as icd-9 code and value
        as the corresponding disease group names
    """

    icd9_encyclopedia_reverseIndex = {}

    for group_name, values in icd9_encyclopedia.items():
        for icd9_code, disease_name in values.items(): 
            icd9_encyclopedia_reverseIndex[icd9_code] = group_name    
    
    return icd9_encyclopedia_reverseIndex


icd9_encyclopedia_reverseIndex = process_icd9_encyclopedia(icd9_encyclopedia)

def summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex):
    """
    args:
        patient_records obtained from process_patient_data("DIAGNOSES_ICD.csv.gz")
        icd9_encyclopedia_reverseIndex from process_icd9_encyclopedia(icd9_encyclopedia)
    returns:
        patient_records_summary: a dictionary with patient ID as key and a list of 
        disease group names as value
    """

    patient_records_summary = {}

    for patID, ICD9_codes in patient_records.items():
        for ICD9_code in ICD9_codes:
            if ICD9_code in icd9_encyclopedia_reverseIndex:
                patient_records_summary.setdefault(str(patID), []).append(icd9_encyclopedia_reverseIndex[ICD9_code])
    
    for key, values in patient_records_summary.items():
        patient_records_summary[key]= (set(values))    

    return patient_records_summary

patient_records_summary = summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex)

# check
print("\n\n**** output ****")
for patId, summary in patient_records_summary.items():
    if patId in ['34','35']:
        print(patId, summary)

# Find similar patients
def getKey1(item): return item[1]

def get_patients_similarity(query_patient_records, patient_records_summary, icd9_encyclopedia_reverseIndex):
    """
    args:
        query_patient_records: same compound type as patient_records but for a test set of patients
        patient_records_summary: dictionary obtained from 
        summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex)
        icd9_encyclopedia_reverseIndex from process_icd9_encyclopedia(icd9_encyclopedia)
    returns:
        patient_similarity: a dictionary with key as test patient ID and value as a list of 2-value tuples
        The first value in the tuple is the neighbor patient ID and the second value in the tuple is the 
        similarity score between the neighbor patient and the test patient
    """    
    
    query_patient_records_summary = summarize_patient_records(query_patient_records, icd9_encyclopedia_reverseIndex)
    
    patient_similarity = {}
    
    for queryID, disease_groups in query_patient_records_summary.items():
        results_tuple = []
        n = 0

        for patID, DiseaseGroups in patient_records_summary.items():
            
            #to ensure the list does not contain the query ID itself 
            if patID != queryID:
                
                # calculate similarity score 
                totalSimilarity = len(disease_groups & DiseaseGroups) - len(disease_groups - DiseaseGroups) - len(DiseaseGroups - disease_groups)
                results_tuple.insert(n,(patID, totalSimilarity))
                n += 1
        
        results_tuple.sort(key=getKey1, reverse=True)
        
        patient_similarity[queryID] = results_tuple    

    return patient_similarity


icd9group_examples = [[295], [332], [491]] # schizo, parkinson, copd
example_disorders_all = set([])
for i in icd9group_examples:
    for j in i:
        example_disorders_all.add(str(j))

query_patient_records = {}
for i in icd9group_examples:
    example_disorders = set([])
    for j in i:
        example_disorders.add(str(j))
    for patId,icd9list in patient_records.items():
        if len(icd9list & example_disorders) > 0 and \
        len(icd9list & (example_disorders_all-example_disorders)) == 0:
            query_patient_records[patId] = icd9list            
            break

print(query_patient_records.keys()) # dict_keys(['71', '85', '111'])

patient_similarity = get_patients_similarity(query_patient_records, 
                                             patient_records_summary, 
                                             icd9_encyclopedia_reverseIndex)

print("\n\n**** output ****")
for k,x in patient_similarity.items():
    print(k, x[0:5])

#71 [('2247', 1), ('1438', 0), ('2183', 0), ('4596', 0), ('750', -1)]
#85 [('5166', 0), ('2061', -1), ('5107', -1), ('4577', -2), ('4676', -2)]
#111 [('4453', 9), ('1598', 6), ('3122', 6), ('5077', 6), ('1038', 5)]
    


# Make diagnosis based on icd9 codes from top k most similar patient
def make_diagnosis(query_patient_records, patient_records_summary, patient_records, top_k=20):
    """
    args:
        query_patient_records: same compound type as patient_records but for a test set of patients
        patient_records_summary: obtained from summarize_patient_records(patient_records)
        patient_records: obtained from process_patient_data("DIAGNOSTIC_CODE.csv.gz")
        top_k: integer value specifiy the number of most closely matched patients to each query patient (default: 20)
    returns:
        query_patient_diagnosis: a dictionary with key as the query patient ID and value as the 
        sorted list of tuples. The first value in the tuple is the icd-9 code and the second value in the 
        tuple is the frequency of icd-9 observed among the top_k matched patient. The list is sorted in _decreasing_ 
        order by the frequency of the ICD-9 code
    """
    
    patient_similarity = get_patients_similarity(query_patient_records, 
                                             patient_records_summary, 
                                             icd9_encyclopedia_reverseIndex)

    query_patient_diagnosis = {}

    # YOUR CODE HERE   
    topMatch = {} #dict containing top_k amount of patient similarities per query ID
    for queryID, disease_groups in query_patient_records.items():
        top_K_matched = patient_similarity[str(queryID)][0:top_k]
        topMatch.setdefault(queryID, top_K_matched)
        
        # set frequency of icd9 codes observed in query patient to 1
        for disease in disease_groups:
            query_patient_diagnosis.setdefault(queryID, []).append((disease, 1))         
    
    for query_ID, topK_patients in topMatch.items():
        Neighbor_icdCodes = {} #dict of each neighbor patient's icd9 codes
        count = {}    #amount of times each icd9 code appears in the top_k patients
        
        for tup in topK_patients:
            neighborID = int(tup[0])
            Neighbor_icdCodes.setdefault(neighborID, patient_records[neighborID])
        
        for key, value in Neighbor_icdCodes.items():

            for icdCode in value:
                if icdCode not in query_patient_records[query_ID]:                                   
                    if icdCode in count:
                        count[icdCode] += 1
                    else:
                        count[icdCode] = 1
             
        SortList = [] #sorted list of tuples: (icd9 code, frequency)
        
        for code, occurence in count.items():
            SortList.append((code, (occurence/top_k)))

        SortList.sort(key=getKey1, reverse=True) #sort in decreasing order by frequency
        
        # append list to query_patient_diagnosis dict
        for n in SortList:
            query_patient_diagnosis[query_ID].append(n)    

    return query_patient_diagnosis

query_patient_diagnosis = make_diagnosis(query_patient_records, patient_records_summary, patient_records)
    
# check 
def getCode_icd9code_Info(icd9_encyclopedia):

    icd9_info = {}

    for k,x in icd9_encyclopedia.items():
        for icd9_code, icd9_names in x.items():
            icd9_info[icd9_code] = {'group':k, 'code':icd9_code, 'name':icd9_names}
    return icd9_info

def write_diagnosis_report(query_patient_diagnosis, query_patient_records, icd9_info, outfile):
    
    f = open(outfile, 'w')

    f.write("patId\tsymptoms_status\ticd9 group\tICD9 code\tICD9 name\tFrequency\n")

    for patId, diagnosis in query_patient_diagnosis.items():

        for icd9 in query_patient_records[patId]:
            
            x = icd9_info[icd9]
            f.write(f"{patId}\tobserved\t{x['code']}\t{x['name']}\t1\n")

        for icd9_tuple in diagnosis:
            icd9_code = icd9_tuple[0]
            icd9_freq = icd9_tuple[1]
            if icd9_freq > 0.2 and icd9_freq < 1 :
                icd9_code_info = icd9_info[icd9_code]
                f.write(f"{patId}\tpredicted\t{icd9_code}\t{icd9_code_info['name']}\t{icd9_freq}\n")
    f.close()

print("\n\n**** output ****")
icd9_info = getCode_icd9code_Info(icd9_encyclopedia)
outfile = "diagnosis_report.txt"
write_diagnosis_report(query_patient_diagnosis, query_patient_records, icd9_info, outfile)
filein = open(outfile, 'r')
for i in range(10):
    line = filein.readline()
    print(line.rstrip())


# evaluate diagnostic predictions to choose the best overall k
all_patient_records = process_patient_data("DIAGNOSES_ICD.csv.gz", max_patients=5000)

train_patient_records = {}
test_patient_records = {}

n_train = 2500

for patId in all_patient_records.keys():
    if len(train_patient_records.keys()) < n_train:
        train_patient_records[patId] = all_patient_records[patId]
    else:
        test_patient_records[patId] = all_patient_records[patId]

def icd9_prediction(target_icd9, test_patient_records, train_patient_records, 
                    icd9_encyclopedia_reverseIndex, top_k = 5):    
    """
    args:
        target_icd9: icd9 code that we will be predicting from a subset of the test_patient_records
        test_patient_records: obtained from process_patient_data("DIAGNOSTIC_CODE.csv.gz")
        train_patient_records: obtained from process_patient_data("DIAGNOSTIC_CODE.csv.gz")
        icd9_encyclopedia_reverseIndex: obtained from process_icd9_encyclopedia(icd9_encyclopedia)
        top_k: integer value specifies the number of most closely matched patients to each query patient (default: 20)
    returns:
        accuracy: a numeric value as the correct predictions divided by the total correct plus incorrect predictions
    """

    train_patient_records_summary = summarize_patient_records(train_patient_records, icd9_encyclopedia_reverseIndex)

    test_patient_records_new = {}

    for patId, icd9code in test_patient_records.items():
        if target_icd9 in icd9code:
            test_patient_records_new[patId] = icd9code - {target_icd9}            

    test_patient_records_controls = {}
    
    for patId, icd9code in test_patient_records.items():
        if target_icd9 not in icd9code:
            test_patient_records_controls[patId] = icd9code            
        if len(test_patient_records_controls) == len(test_patient_records_new):
            break
    
    test_patient_records_new.update(test_patient_records_controls)

    test_patient_diagnosis = make_diagnosis(test_patient_records_new, 
        train_patient_records_summary, train_patient_records, top_k)

    correct = 0
    incorrect = 0
    
    for j  in test_patient_records_new:  

        if target_icd9 in test_patient_records[j]:
            
            found = False            
            for tup in test_patient_diagnosis[j]:                
                if str(tup[0]) == str(target_icd9): 
                    found=True
                    if tup[1] > (1/top_k):
                        correct += 1                        
                    break
            if not found:
                incorrect += 1                
        else:   
            found = False
            for tup in test_patient_diagnosis[j]:         
                if target_icd9 in tup:
                    if str(tup[0]) == str(target_icd9):
                        found=True
                        if tup[1] > (1/top_k):
                            incorrect += 1
                        break
            if not found:
                correct += 1    
       
    accuracy = correct/(correct+incorrect)
    
    return accuracy

# test
accuracies = {}

icd9_target_list = ['295','332','491']

for target_icd9 in icd9_target_list:
    accuracies[target_icd9] = icd9_prediction(target_icd9, 
              test_patient_records, train_patient_records, 
              icd9_encyclopedia_reverseIndex, top_k = 20)

print("\n\n**** output ****")
for icd9,accuracy in accuracies.items():
    print(f"{icd9}: {100*accuracy:.0f}%")
    
# Choose best k
topk_list = [1, 5, 10, 20, 50, 100, 200, 300, 400, 500]

accuracy_mat = []

for top_k in topk_list:    
    accuracy_list = []
    for target_icd9 in icd9_target_list:                
        accuracy = icd9_prediction(target_icd9, test_patient_records, train_patient_records, 
                        icd9_encyclopedia_reverseIndex, top_k = top_k)
        
        accuracy_list.append((target_icd9, accuracy))
    
    accuracy_mat.append(accuracy_list)

performance = []

for i in range(len(topk_list)):
    my_sum = 0
    for j in range(len(accuracy_mat[i])):
        my_sum += accuracy_mat[i][j][1]        
    performance.append((topk_list[i], my_sum/len(accuracy_mat[i])))
    
print("\n\n**** output ****")
print("K is sorted by accuracy:")
performance.sort(key=getKey1, reverse=True)

for k,acc in performance:
    print(f"{k}: {100*acc:.0f}%")





