def NeurDisorder(ND):
    if ND == "Yes":
        temperature(input("body temp (°C)? "))
    elif ND == "No":                      
        print("low-risk")       
    else:
        print("invalid")        

def temperature(T): #Function to check if user's value is a float or a string. 
    if T.isdecimal():
        tempFloat = float(T)
        if tempFloat < 38:   
            CRP(input("CRP (mg/dl): "))
        elif tempFloat >= 38:
            ADA2(input("ADA2 pathogenic mutations (0 pathogenic mutations; 1 pathogenic mutation or 2 bialellic pathogenic mutations)? "))

    elif not T.isdecimal():
        templist = T.split('.')     
        if templist[0].isdecimal() and templist[1].isdecimal():
            tempFloat = float(T)
            if tempFloat <38.0:
                CRP(input("CRP (mg/dl): "))                                                
            elif tempFloat >= 38.0:
                ADA2(input("ADA2 pathogenic mutations (0 pathogenic mutations; 1 pathogenic mutation or 2 bialellic pathogenic mutations)? "))                  
        else:
            print("invalid")

def CRP(C):
    if C.isdecimal():
        CRPFloat = float(C)
        if CRPFloat >= 5:
            ADA2(input("ADA2 pathogenic mutations (0 pathogenic mutations; 1 pathogenic mutation or 2 bialellic pathogenic mutations)? "))
        elif CRPFloat <5:
            print("low-risk")
    
    elif not C.isdecimal(): 
        CRPlist = C.split('.') 
        if CRPlist[0].isdecimal() and CRPlist[1].isdecimal():  
            CRPFloat = float(C)
            if CRPFloat >= 5:   
                ADA2(input("ADA2 pathogenic mutations (0 pathogenic mutations; 1 pathogenic mutation or 2 bialellic pathogenic mutations)? "))
            elif CRPFloat <5: 
                print("low-risk")
    
        else:
            print("invalid")       
            
def ADA2(mutNumber):
    if mutNumber == "0 pathogenic mutations":
        print("low-risk")
    elif mutNumber == "1 pathogenic mutation":
        print("medium-risk")
    elif mutNumber == "2 bialellic pathogenic mutations":
        print("high-risk") 
    else:
        print("invalid")     

liveSkinRash = input("Livedoid skin rash (Yes or No)? ") #starts here 
if liveSkinRash == "No":    
    NeurDisorder(input("Neurological disorder (Yes or No)? "))   
elif liveSkinRash== "Yes":
    temperature(input("body temp (°C)? "))
else:
    print("invalid")


