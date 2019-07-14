import requests
from bs4 import BeautifulSoup
import getpass
import os
import json

data = {'ctl00$MainContent$UserName': '', 'ctl00$MainContent$Password': '','ctl00$MainContent$Button1':'Log In'}
data1="__VIEWSTATE=%2FwEPDwUJLTYyNDUwMzcxD2QWAmYPZBYCAgMPZBYCAnMPZBYCAgEPFgIeBFRleHRlZGT9VtEXp1Es8cwarY9rixrHn0whYYK1i2lfOKIg3WDRhg%3D%3D&__VIEWSTATEGENERATOR=6B7E562E&__EVENTVALIDATION=%2FwEdAAZTvk6hwaqsUL3ogtzXrAZX45a3adTEMpbjbWP0qDUy5sfvyjIx4eNfJAMrZe%2FGRMD%2FtZrOiYJPSwQdWShmXqFGz70%2FezTD4x4Y4%2BibsTHKkPnd3wctyww89JbDbeLvgriKqU1TOU%2BOcSDK6D9EpFhPPuzU3uMwvx6%2FUC02NNYx%2FA%3D%3D&ctl00%24MainContent%24User=Student&ctl00%24MainContent%24UserName=ECA1713710&ctl00%24MainContent%24Password=w1se0977&ctl00%24MainContent%24Button1=Log+In"
# A Session object will persist the login cookies.
login = "https://sms.unilus.ac.zm/Students/Login.aspx"
studentPortal = "https://sms.unilus.ac.zm/Students/StudentPortal.aspx"
ca="https://sms.unilus.ac.zm/Students/ViewCA.aspx"
assignments_link = "https://sms.unilus.ac.zm/Students/Assignments.aspx"
reg_form = "https://sms.unilus.ac.zm/Students/RegistrationForm.aspx"
user=getpass.getuser()
drive = os.getenv("SystemDrive")
absolutepath=drive+"\\Users\\"+user+"\\Documents\\Classmate\\"
performance_path=absolutepath+"stand.cmt"

if not os.path.exists(absolutepath):
    os.makedirs(absolutepath)

def getCookieFile():
    with open(absolutepath+"cookie.cmt","r")as cf:

        return cf.read()
def getCredentials():
    with open(absolutepath+"dentials.cmt","r")as cf:
        cf=cf.read()
        return eval(cf)
def auth(base_url, target_url, username, password):
    with requests.Session() as s:
        page = s.get(base_url)
        s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        s.headers["Host"]="sms.unilus.ac.zm"
        soup = BeautifulSoup(page.content,"html.parser")
        data["ctl00$MainContent$UserName"]=username
        data["ctl00$MainContent$Password"]=password
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
        print(s.headers)

        s.post(base_url, data=data)
        open_page = s.get(target_url)

        #Check content
        if str(open_page.text).__contains__("action=\"./Login.aspx\""):
            with open(absolutepath+"test.html","w")as test:
                test.write(str(open_page.text))

            return "fail","Credential Error"
        else:
            # stotr session
            #  id and return
            with open(absolutepath+"cookie.cmt","w")as cookieFile:
                cookieFile.write(s.cookies["ASP.NET_SessionId"])

            with open(absolutepath+"dentials.cmt","w")as credentialsFile:
                credentialsFile.write(str({"username":username,"password":password}))

            return "success",open_page.text

def access(target_url):

    with requests.Session() as s:
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
#         get cookie
        cookie=getCookieFile()
        print(cookie)
        s.cookies["ASP.NET_SessionId"]=cookie
        html=s.get(target_url).text
        credentials=getCredentials()

        if str(html).__contains__("./Login.aspx"):
            s.close()
            attemptReLogin=auth(login,target_url,credentials["username"],credentials["password"])
            if attemptReLogin[0]=="fail":

                return "fail","Server or Credential error"
            else:

                return "success", attemptReLogin[1]
        else:
            print("retri2")
            return "success", html

def getRegistrationData():
    returned = access(reg_form)
    if returned[0]=="fail":
        return returned

    soup = BeautifulSoup(returned[1],"html.parser")
    form = soup.find(id = "divPrint")
#     get all tds
    tds = form.find_all("td")
    program = ""
    year = ""
    semester = ""
    mode = ""
    for td in tds:
        if str(td).lower().__contains__("program of study"):
            program = str(td.get_text()).replace("PROGRAM OF STUDY ","")

        if str(td).lower().__contains__("mode of study"):
            mode = str(td.get_text()).replace("MODE OF STUDY ","")
        elif str(td).lower().__contains__("semester"):
            year_sem = []
            for  i  in range(str(td.get_text()).__len__()):
                try:
                    year_sem.append(int(td.get_text()[i]))
                except:
                    continue
            semester = year_sem[1]
            year = year_sem[0]

    rows = soup.select("tr[class^=grd]")
    courses={"courses":{},"mode":mode,"year":year,"semester":semester,"program":program}

    if program=="" and year =="" and semester =="" and mode =="":
        return "fail"
    for row in rows:
        cols = row.find_all("td")
        code = str(cols[1].get_text()).split(" ",-1)[1]
        courses["courses"][code]={"code":str(cols[1].get_text()).split(" ",-1)[1],"name":cols[2].get_text(),"material":[],"assignments":[],"performance":{"CA":
                    {"assignment":"","practical":"","mid":"","total":""},"Final":""},"lecturerInfo":{"email":"","phone":""}}
    with open(absolutepath+"mation.cmt","w")as info:
        json.dump(courses,info)
    return "success"


def getAssignments():
    returned = access(assignments_link)
    if returned[0]=="fail":
        return returned

    soup = BeautifulSoup(returned[1],"html.parser")
    rows = soup.select("tr[class^=grd]")
    keys = ["year","assignmentNumber","course","description","SubmittedDate","DueDate"]
    info=""
    with open(absolutepath+"mation.cmt","r") as info:
        info=json.load(info)


    for row in rows:
        cols = row.find_all("td")
        info["courses"][cols[2].get_text()]["assignments"].append({"year":cols[0].get_text(),"assignmentNumber":cols[1].get_text(),"description":cols[3].get_text(),"submittedDate":cols[4].get_text(),"dueDate":cols[5].get_text()})
        count=count+1



    with open(absolutepath+"mation.cmt","w") as info_f:
        json.dump(info,info_f)

    return "success"

def getCaData():
    returned=access(ca)
    if returned[0]=="fail":
        return returned
    soup=returned[1]

    soup = BeautifulSoup(soup,"html.parser")
    rows = soup.select("tr[class^=grd]")
    keys = ["Course","Assignment","Practical","Mid","CA"]

    info=""
    with open(absolutepath+"mation.cmt","r") as info:
        info=json.load(info)
    count = 0
    for row in rows:
        cols = row.find_all("td")
        print("here",info)
        info["courses"][cols[0].get_text()]["performance"]["CA"]["assignment"]=cols[1].get_text()
        info["courses"][cols[0].get_text()]["performance"]["CA"]["practical"] = cols[2].get_text()
        info["courses"][cols[0].get_text()]["performance"]["CA"]["mid"] = cols[3].get_text()
        info["courses"][cols[0].get_text()]["performance"]["CA"]["total"] = cols[4].get_text()
        count = count+1

    if count==0:
        return "fail"


    with open(absolutepath+"mation.cmt","w") as info_f:
        json.dump(info,info_f)
    return "success"

# called when on refresh of all info and on first login
# def getAll(username, password):



# getAssignments()
#
# print(auth("https://sms.unilus.ac.zm/Students/Login.aspx","https://sms.unilus.ac.zm/Students/StudentPortal.aspx"
#        ,"ECF1712794","218"))
