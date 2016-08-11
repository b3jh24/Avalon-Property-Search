'''
Created on Aug 11, 2016

@author: BHornak
'''
from mechanize import Browser
from bs4 import BeautifulSoup
from Tkinter import *
import tkFileDialog

filePath = ""
master = Tk()
master.title("Avalon Property Search")
master.geometry("610x150+500+300")
Label(text="Output file name: ",pady=20).grid(row=0,column=0)
fileNameEntry = Entry(master,width=35)
fileNameEntry.grid(row=0,column=1,padx=10,pady=5)
fileNameEntry.insert(0, filePath)


def askForFileSaveLocation():
    fileNameEntry.delete(0, END)
    filePath = tkFileDialog.asksaveasfilename()
    fileNameEntry.insert(0,filePath)
    fileNameLength = len(fileNameEntry.get())
    numToShiftBy = fileNameEntry.winfo_width() - fileNameLength
    fileNameEntry.xview_scroll(numToShiftBy,UNITS)

changeSaveLocation = Button(master,text="Save as...",command=askForFileSaveLocation)
changeSaveLocation.grid(row=0, column=2,padx=10)

Label(text="Street Address: ").grid(row=1, column=0,sticky=W)
streetNameEntry=Entry(master,width=35)
streetNameEntry.grid(row=1,column=1,padx=10,pady=5)

def submitForm():
    br = Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    br.open("http://njparcels.com/search/")
    br.select_form(nr=0)
    
    br.form['s'] = streetNameEntry.get()
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
        ownerFile.write("\nAvalon residence: "+ streetNameEntry.get())
        ownerFile.write("\n\n")
    
    with open("tes.html","wb") as t:
        t.write(resp.read())
    
    master.quit()

submit = Button(master,text="Submit",command=submitForm)
submit.grid(row=1, column=2,sticky=W,padx=10)

mainloop()



    