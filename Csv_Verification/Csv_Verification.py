import csv;
import datetime
from datetime import date


def ExtractVars(format):
    extracted = []
    temp = ""
    flag = False
    
    for i in format:
        if i=="%":
            if (flag==True):
                extracted.append(temp)
            flag = not flag
            temp=""
        elif (flag==True):
                temp+=i
    
    return extracted

def replaceFilename(format, billerId, dateVar, ouId):
    result = format
    splittedFormat = format.split("%")
    customDates = []
    for i in splittedFormat:
         if "date" in i :
              customDates.append(i)

    for i in customDates:
         result.replace(i, str(dateVar))  

    result = result.replace("%billerid%", str(billerId))
    result = result.replace("%ouid%", str(ouId))
    
    return result



def ValidFileFormat(format):
    extracted = ExtractVars(format)
    validVars = ["billerid", "date","date(ddMMyyyy)", "ouId"]
    l=[]
    c = format.count("%")

    if (c%2 != 0):
        return False
    
    for i in extracted:
         if i not in validVars:
              return False
     

with open("C:\\Users\\MYPC\\Desktop\\hatio\\arjun_Tasks\\Csv_Verification\\Book.csv", mode="r", newline='') as csvfile:
    reader = csv.reader(csvfile)
    billerIds=[]
    dates = []
    formats = []
    ouIds = []
    firstRow = False
    for row in reader:
        if firstRow == False:
                firstRow = True
                continue
        else:
            billerIds.append(row[2])
            dates.append(row[4])
            formats.append(row[1])
            ouIds.append(row[3])


for i in range(len(formats)):
    format = formats[i]
    billerId = billerIds[i]
    dateVar = dates[i]
    ouId = ouIds[i]
    if ValidFileFormat(format) ==False:
        print(format, "Invalid")
        break
    print(replaceFilename(format, billerId, dateVar))
    
  
    


