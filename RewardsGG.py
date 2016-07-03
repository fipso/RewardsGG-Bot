import pycurl
import os
import os.path
import time
import random
import threading
import shutil
import re
from io import BytesIO

UserList = []
debug = False

class BotUser:

    def __init__ (self, username, password):
        self.username = username;
        self.password = password;

    def printData():
        print (username + ":" + password)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def addTicket(url, user):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.COOKIEFILE, "cookies/" + user.username + ".cookie")
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
    c.setopt(pycurl.HTTPHEADER, ["X-Requested-With: XMLHttpRequest"])
    c.perform()
    c.close()

    body = buffer.getvalue()
    text = body.decode("iso-8859-1")

    if debug:
        print("[DEBUG]:\n" + text)

def cookieThread():
    while 1 == 1:
        for user in UserList:

            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, "https://rewards.gg/login")
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.COOKIEJAR, "cookie.tmp")
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
            c.perform()
            c.close()

            body = buffer.getvalue()
            text = body.decode("iso-8859-1")

            csrfToken = find_between(text, 'name="_csrf_token" value="', '"')

            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, "https://rewards.gg/login_check")
            c.setopt(pycurl.COOKIEFILE, "cookie.tmp")
            c.setopt(pycurl.COOKIEJAR, "cookies/" + user.username + ".cookie")
            c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/x-www-form-urlencoded"])
            c.setopt(pycurl.POSTFIELDS, "csrf_token=" + csrfToken + "&_username=" + user.username + "&_password=" + user.password + "&_submit=Login")
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.perform()
            c.close()

            body = buffer.getvalue()
            text = body.decode("iso-8859-1")

            if debug:
                print("[DEBUG]:\n" + text)

            if text.find(user.username) == -1:
                print("[WARNING] Login as " + user.username + " failed")

            time.sleep(5)
        time.sleep(60*60*24)

def earnThread():
    ad = 5
    while 1 == 1:
        for user in UserList:
            while os.path.isfile("cookies/" + user.username + ".cookie") == False:
                time.sleep(10)

            addTicket("https://rewards.gg/user/addTickets", user)
            time.sleep(5)

            if ad >= 5:
                ad = 0
                addTicket("https://rewards.gg/user/add-adv-click-tickets", user)
                time.sleep(5)
                addTicket("https://rewards.gg/user/add-job-offer-ticket", user)

        ad += 1
        time.sleep(785)

def getGameID(url):
    buffer=BytesIO()
    c= pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.WRITEDATA,buffer)
    c.setopt(pycurl.SSL_VERIFYPEER,0)
    c.setopt(pycurl.SSL_VERIFYHOST,0)
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
    c.perform()
    c.close()

    body=buffer.getvalue()
    text=body.decode("iso-8859-1")

    pattern = 'data-gvid="(.+?)"'
    gid = re.search(pattern,str(text))

    return gid.group(1)


print("[INFO] Starting...")

with open("accounts.secure") as f:
    accountList = f.readlines()

for line in accountList:
    words = line.strip()
    words = words.split('|')
    user = BotUser(words[0],words[1])
    UserList.append(user)

folder = 'cookies/'

if not os.path.exists(folder):
    os.makedirs(folder)

for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print("[ERROR] " + e)

threading._start_new_thread(cookieThread, ())
threading._start_new_thread(earnThread, ())

print("[INFO] Ready")

while 1 == 1:
    userInput = input(">")
    if userInput == "tickets":
        total = 0
        for user in UserList:
            while os.path.isfile("cookies/" + user.username + ".cookie") == False:
                time.sleep(1)

            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, "https://rewards.gg/")
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            c.setopt(pycurl.COOKIEFILE, "cookies/" + user.username + ".cookie")
            c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
            c.perform()
            c.close()

            body = buffer.getvalue()
            text = body.decode("iso-8859-1")

            tickets = find_between(text, 'class="tickets-count">' , '</')
            if tickets != "":
                print ("[INFO] " + user.username + " has " + tickets + " tickets")
                total = total + int(tickets)
            else:
                print ("[ERROR] could not get tickets for " + user.username)

        print("\n[INFO] Total avaible tickets: " + str(total))

    elif userInput == "debug":
        if debug:
            print("[INFO] disabled debug mode")
            debug = False
        else:
            print("[INFO] enabled debug mode")
            debug = True

    elif userInput.startswith("spent"):
        if len(userInput.split(' ')) >= 4:
            words = userInput.split(' ')
            for user in UserList:
                while os.path.isfile("cookies/" + user.username + ".cookie") == False:
                    time.sleep(1)
                if user.username == words[3]:
                        gid = getGameID(words[1])
                        buffer = BytesIO()
                        c = pycurl.Curl()
                        c.setopt(pycurl.URL, "https://rewards.gg/user/participate?preventCache=Sun%20May%2001%202016%2022:30:08%20GMT+0200%20(Mitteleurop%C3%A4ische%20Sommerzeit)&gid=" + gid + "&tickets=" + words[2])
                        c.setopt(pycurl.WRITEDATA, buffer)
                        c.setopt(pycurl.SSL_VERIFYPEER, 0)
                        c.setopt(pycurl.SSL_VERIFYHOST, 0)
                        c.setopt(pycurl.COOKIEFILE, "cookies/" + user.username + ".cookie")
                        c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
                        c.setopt(pycurl.HTTPHEADER, ["X-Requested-With: XMLHttpRequest"])
                        c.perform()
                        c.close()

                        body = buffer.getvalue()
                        text = body.decode("iso-8859-1")

                        if debug:
                            print("[DEBUG]:\n" + text)
                            print("[DEBUG]: Game ID: " + gid)

                        print("[INFO] spent " + words[2] + " tickets on ID: " + gid)

        else:
            print("[INFO] usage: spent <itemURL> <amount> <account>")

    elif userInput == "fix":
        for user in UserList:
            while os.path.isfile("cookies/" + user.username + ".cookie") == False:
                time.sleep(1)
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, "https://rewards.gg/get-tickets")
            c.setopt(pycurl.COOKIEFILE, "cookies/" + user.username + ".cookie")
            c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            c.perform()
            c.close()

            body = buffer.getvalue()
            text = body.decode("iso-8859-1")

            if debug:
                print("[DEBUG]:\n" + text)

            print("[INFO] attempting to solve problems for " + user.username)

    elif userInput == "quit":
        break

    elif userInput == "exit":
        break

    elif userInput != "":
        print("[ERROR] command not found")
