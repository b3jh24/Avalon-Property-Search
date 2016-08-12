'''
Created on Aug 12, 2016

@author: BHornak
'''
import xlsxwriter
from fileinput import close

address = ""
city = ""
state = ""
zipc = ""

infoFile = open("owner_info.txt", 'rb')

def WriteSpreadsheet(addressList, cityList, stateList):
    #Create workbook
    workbook = xlsxwriter.Workbook('Addresses.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1,1,15)
    
    #Create headers
    col = 0
    row = 1
    headers = ["Address","City","State"]
    for h in headers:
        worksheet.write(0, col,    h)
        col += 1
    
    #Fill data
    for addr in addressList:
        worksheet.write(row, 0,     addr)
        row += 1
    row = 1
    for city in cityList:
        worksheet.write(row,1,      city)
        row += 1
    row = 1
    for state in stateList:
        worksheet.write(row,2,      state)
        row += 1
    
    workbook.close()

def getNumberOfHomes(infoFile):
    i = 0
    localFile = infoFile
    localFile.seek(0)
    for line in localFile:
        line = line.replace("\n","")
        if line == "\r":
            continue
        else:
            i+=1
    numHomes = i / 3
    return numHomes

def parseFile(infoFile):
    listSize = getNumberOfHomes(infoFile)
    addressList = [""] * listSize
    cityList = [""] * listSize
    stateList = [""] * listSize
    
    currentListIndex = 0
    '''Parse the text file for the address information and do stuff with it'''
    global address,city,state,zipc
    
    infoFile.seek(0)    
    currentLineNum = 0
    for line in infoFile:
        line = line.replace("\n","")
        if line == "\r":
            continue
        if currentLineNum == 1:
            myLine = line
            #Get all the info and store them properly from the line containing the address
            strip = myLine.lstrip("Owner's address: ")
            index = strip.index(',')
            lastCommaIndex = strip.rindex(',')
            leng = len(strip)
            address = strip[:index]
            addressList[currentListIndex] = address
            city = strip[index+2:lastCommaIndex]
            cityList[currentListIndex] = city
            state = strip[leng-3:leng-1]
            stateList[currentListIndex] = state
            currentListIndex += 1
        currentLineNum +=1    
        if currentLineNum == 3:
            currentLineNum = 0
    
    WriteSpreadsheet(addressList, cityList, stateList)
    
parseFile(infoFile)
infoFile.close()