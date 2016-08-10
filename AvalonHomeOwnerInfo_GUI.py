import re 
from mechanize import Browser
from bs4 import BeautifulSoup
from Tkinter import *
from random import randint
import webbrowser
import time

'''Global Objects'''
br = Browser()

pword = "P4ssword"
email = ""
address = ""
captcha = ""


master = Tk()
master.title("Avalon Property Search")
master.geometry("400x150")
Label(text="Output file name: ",pady=20).grid(row=0,column=0)
fileNameEntry = Entry(master,width=25)
fileNameEntry.grid(row=0,column=1,padx=10,pady=5)
fileNameEntry.insert(0, "ownerInfo.txt")

Label(text="Street Address: ").grid(row=1, column=0,sticky=W)
streetNameEntry=Entry(master,width=25)
streetNameEntry.grid(row=1,column=1,padx=10,pady=5)
'''--------------'''
def setcaptcha(localCaptcha):
    global captcha
    captcha = localCaptcha
    print ":" + captcha

def getcaptcha():
    global captcha
    return captcha

def createCaptchaWindow():
    master.destroy()
    top = Tk()
    top.geometry("300x100")
    top.title("CAPTCHA")
    Label(top,text="Enter captcha: ",pady=20).grid(row=0,column=0)
    captchaEntry = Entry(top, width=15)
    captchaEntry.grid(row=0, column=1,padx=10,pady=5)
    Button(top,text="Submit",command=lambda: setcaptcha(captchaEntry.get())).grid()

def getStreetAddress():
    global address
    address = streetNameEntry.get()
    generateEmail()

def generateEmail():
    """Create a new email from mailnesia.com
    
    Return: email - a string containing the email address
    """
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    email_site = br.open( "http://mailnesia.com/" )
    link = br.find_link(url='/random/')
    inbox = br.follow_link(link)
    soup = BeautifulSoup(inbox, 'html.parser')
    header = soup.find('h1', {"class" : "emails"})
    stuff = header.find('a')
    emailText = stuff.get_text()
    global email
    email = emailText+"@mailnesia.com"
    createAccount()
    
def getReport(homePage):
    """Fill out the house-lookup form on PropertyShark and open the report"""  
    global address
    url = homePage.geturl()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    br.open(url)
    br.select_form(nr=0)
    br.form['search_token'] = address
    br.form['location'] = 'Avalon, NJ'
    reportPage = br.submit()
    soup = BeautifulSoup(reportPage,'html.parser')
    stuff = soup.find('a', {"class" : "onepager"})
    onepageReportLink = stuff.get('href')
    #webbrowser.open_new("http://www.propertyshark.com"+onepageReportLink)
    onepageReport = br.open("http://www.propertyshark.com"+onepageReportLink)
    reportSoup = BeautifulSoup(onepageReport,'html.parser')
    data = reportSoup.find('div', {"id": "nationwide/owner_and_sale_content"})
    #print data
    dataTable = data.find('table', {"class": "data"})
    i = 0
    for info in dataTable.find_all('td'):
        if i == 1:
            ownerName = info.get_text()
        elif i == 3:
            ownerAddress = info.get_text()
        i += 1
    with open("owner_info.txt", 'a') as dataFile:
        dataFile.write("Owner's name: "+ownerName)
        dataFile.write("\nOwner's address: "+ownerAddress)
        dataFile.write("\nAvalon Address: " + address+"\n")
    
def login():
    """Login to PropertyShark once account has been activated"""
    time.sleep(50)
    print "Email: " + email
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    propShark = br.open("https://secure.propertyshark.com/mason/Accounts/logon.html")
    br.select_form(nr=0)        #just select an initial form to activate
    br.form['email'] = email
    br.form['password'] = pword
    page = br.submit()
    #DEBUG
    with open("web.html", "wb") as f:
        f.write(page.read()) 
    
    getReport(page)    
    
    
def createAccount():
    """Create an account on the PropertyShark page and create a text file with login credentials
    An account requires a name, email, password, phone number, role in real estate, captcha, and agree to terms (in order)
    """
    names = ["Brian Smith", "Scott Walker", "Mike Herman", "Dan Gleesac"] #List of names to choose from
    nameToUse = names[randint(0,3)]     #Pick a random name for the account
    #pword = "P4ssword"
    phoneNumber = "201-785-0981"
    
    '''Process is as follows:
    
    -User enters street address (handled in a separate function)
    -Open generic PropertyShark web page for account creation
    -Create account based on info here
    -Activation email is sent to mailnesia email (and opened automatically)
    -Login to PropertyShark using credentials here (email + password)
    -Enter street address on form
    -Report provided (do stuff with or whatever)
    
    '''
    
    #Go to the Property Shark account creation page
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    propShark = br.open("https://secure.propertyshark.com/mason/Accounts/edit_user_info.html")
    br.select_form(nr=0)        #just select an initial form to activate
    br.form['name'] = nameToUse
    br.form['email'] = email
    br.form['password'] = pword
    br.form['phone'] = phoneNumber
    br.form['profession'] = ['Homebuyer']
    
    #Find the captcha image
    soup = BeautifulSoup(propShark, "html.parser")
    captchaDiv = soup.find('div', {"class" : "captcha_img_cont"})
    #print captchaDiv
    img = captchaDiv.find_all()[0]['src']
    #print "Image: "
    #Append the image location to the main body URL
    img = "https://secure.propertyshark.com"+img
    #print img
    #Open the image in a new tab
    webbrowser.open_new_tab(img)
    #TODO: Figure out a way to solve the captcha programmatically instead of having user do it
    createCaptchaWindow()
    br.form['captcha'] = getcaptcha()    
    print "Captcha: "+getcaptcha()
    br.find_control("check_terms").items[0].selected = True
    
    #DEBUG
#     print "\n"
#     for f in br.forms():
#         print f
    response = br.submit()
    
    with open("file.html", 'wb') as fi:
        fi.write(response.read())
    
    #login()

submit = Button(master,text="Submit",command=getStreetAddress)
submit.grid(row=2, column=1)

mainloop()

