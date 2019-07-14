import requests
from bs4 import BeautifulSoup
import webbrowser
import os
def access():
    with requests.Session() as s:

        s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        s.headers["Host"]="www.betpawa.co.zm"
        s.headers["Cookie"]="_ym_uid=1540639686904977979; _ym_d=1540639686; DeviceUsers=a9c4d2ba-e4a9-42f3-8a1b-8e76327f; LoginPhoneNumber=970519299; _fbp=fb.2.1549099851505.200332649; _ym_isad=2; JSESSIONID=83BD1B6C46FDDDB81EE650A79183E56A; sport-selector=3"

        # data["ctl00$MainContent$UserName"]=username
        # data["ctl00$MainContent$Password"]=password
        # data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        # data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        # data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
        # print(s.headers)

        page = s.get("https://www.betpawa.co.zm/jackpot#324-emPawa17",allow_redirects = True)
        soup = BeautifulSoup(page.text,"html.parser")
        print(soup)
        with open("./trial.html","w")as trial:
            trial.write(str(soup))
            webbrowser.open("file://"+os.path.realpath("./trial.html"))
access()