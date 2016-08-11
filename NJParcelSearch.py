'''
Created on Aug 11, 2016

@author: BHornak
'''
from mechanize import Browser
from bs4 import BeautifulSoup
from Tkinter import *
import tkFileDialog

filePath = ""
numberOfProps = 1

master = Tk()
master.title("Avalon Property Search")
master.geometry("640x170+500+300")

Label(text="Output file name: ",pady=20).grid(row=1,column=0,sticky=W)
fileNameEntry = Entry(master,width=35)
fileNameEntry.grid(row=1,column=1,padx=10,pady=5)
fileNameEntry.insert(0, filePath)

Label(text="Street Address: ").grid(row=2, column=0,sticky=W)
streetNameEntry=Entry(master,width=35)
streetNameEntry.grid(row=2,column=1,padx=10,pady=5)

streetEntryList = []
streetEntryList.append(streetNameEntry)

def addStreetEntries(*args):
    global numberOfProps
    global submit
    numberOfProps = int(var.get())
    if(numberOfProps == 1):
        return
    sizeToIncrease = 45 * numberOfProps
    originalWindowLength = 170
    newSize = originalWindowLength + sizeToIncrease
    master.geometry("640x"+str(newSize)+"+500+300")
    for i in xrange (1, numberOfProps):
        lb = Label(text="Street address "+str(1+i)+": ").grid(row=2+i,column=0,pady=15, sticky=W)
        e = Entry(master,width=35)
        e.grid(row=2+i,column=1,padx=10,pady=5)
        streetEntryList.append(e)
    
    submit.grid(row=2+i, column=2,sticky=W,padx=10)
var = StringVar(master)
var.set("1") # initial value
Label(text="Number to search for: ").grid(row=0, column=0)
numSearchList = OptionMenu(master, var,"1","2","3","4","5")
numSearchList.grid(row = 0, column = 1,sticky=W,padx=10)
var.trace("w", addStreetEntries)


def askForFileSaveLocation():
    fileNameEntry.delete(0, END)
    filePath = tkFileDialog.asksaveasfilename()
    fileNameEntry.insert(0,filePath)
    fileNameLength = len(fileNameEntry.get())
    numToShiftBy = fileNameEntry.winfo_width() - fileNameLength
    fileNameEntry.xview_scroll(numToShiftBy,UNITS)

changeSaveLocation = Button(master,text="Save as...",command=askForFileSaveLocation)
changeSaveLocation.grid(row=1, column=2,padx=10)


def submitForm():
    global numberOfProps
    propertyList = [""] * numberOfProps
    #Fill out the property list
    for i in xrange(0,len(propertyList)):
        propertyList[i] = streetEntryList[i].get()
    for i in xrange(0,len(propertyList)):
        br = Browser()
        br.set_handle_robots( False )
        br.addheaders = [('User-agent', 'Firefox')]
        br.open("http://njparcels.com/search/")
        br.select_form(nr=0)
        
        br.form['s'] = propertyList[i]
        br.form['s_co'] = ['05']        #05 is the way the site treats Cape May County in the selection list
        
        resp = br.submit()
        
        """Get owner name and permanent residence"""
        soup = BeautifulSoup(resp,'html.parser')
        ownerTable = soup.find('table', {"class":"table"})
        i =0
        for link in ownerTable.find_all('a'):
            if i == 4:
                ownerName = link.get_text()       #Owner name
            i += 1
        # Get permanent address
        j = 0
        for div in ownerTable.find_all('div'):
            if j == 2:
                #If I just do div.get_text(), it doesn't get the address correctly since there is a <br/> tag in the address to put it on a new line. When actually getting the text,
                #it gets treated as one line, so the address isn't separated from the town, so I have to do it this way instead
                divObjects = div
                m = 0
                for obj in divObjects:
                    #Ignore the <br/> tag
                    if obj == soup.br:
                        continue
                    else:
                        if m == 0:
                            ownerStreet = obj
                        elif m == 1:
                            ownerTown = obj
                    m += 1
            j += 1
        
        filePath = fileNameEntry.get()
        with open(filePath,"a") as ownerFile:
            ownerFile.write("Owner's name: "+ownerName)
            ownerFile.write("\nOwner's residence: "+ ownerStreet+" ")
            ownerFile.write(ownerTown)
            ownerFile.write("\nAvalon residence: "+ propertyList[i])
            ownerFile.write("\n\n")
        
        with open("tes.html","wb") as t:
            t.write(resp.read())
    
    master.quit()

submit = Button(master,text="Submit",command=submitForm)
submit.grid(row=2, column=2,sticky=W,padx=10)

mainloop()



    