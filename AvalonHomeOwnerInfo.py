import re 
from mechanize import Browser
from bs4 import BeautifulSoup
from Tkinter import Tk
from random import randint
from captcha_solver import CaptchaSolver
import webbrowser
import time

'''Global Objects'''
br = Browser()

pword = "P4ssword"
email = ""
address = ""

# Setup and clear clipboard
r = Tk()
r.withdraw()
r.clipboard_clear()
'''--------------'''

def getStreetAddress():
    global address
    address =  raw_input("Enter the street address of the house you want to look at: ")
    print address

# def copyEmailToClipboard():
#     """Copy the 10MinuteMail email address to the clipboard for later use"""
#     br.set_handle_robots( False )
#     br.addheaders = [('User-agent', 'Firefox')]
#     email_site = br.open( "https://10minutemail.com/10MinuteMail/index.html?dswid=-3903" )
#     soup = BeautifulSoup(email_site, "html.parser")
#     mydivs = soup.find('div', {'class' : 'mail-address'})
#     val = mydivs.find_all(id="mailAddress")[0]['value']
#     r.clipboard_append(val)
#     

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
    #webbrowser.open(reportPage.geturl())
    soup = BeautifulSoup(reportPage,'html.parser')
    #print soup
    stuff = soup.find('a', {"class" : "onepager"})
    onepageReportLink = stuff.get('href')
    webbrowser.open_new("http://www.propertyshark.com"+onepageReportLink)
    onepageReport = br.open("http://www.propertyshark.com"+onepageReportLink)
    reportSoup = BeautifulSoup(onepageReport,'html.parser')
#     print "\n------------------REPORT SOUP------------------\n"
#     print reportSoup
    data = reportSoup.find('div', {"id": "nationwide/owner_and_sale_content"})
    print "\n------------------DATA------------------\n"
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
    captcha = raw_input("Enter captcha: ")      #Get captcha from the user
    br.form['captcha'] = captcha    
    br.find_control("check_terms").items[0].selected = True
    
    #DEBUG
#     print "\n"
#     for f in br.forms():
#         print f
    response = br.submit()
    
    with open("file.html", 'wb') as fi:
        fi.write(response.read())

getStreetAddress()
generateEmail()
createAccount()
login()
