import webbrowser
import time

import requests
from bs4 import BeautifulSoup

url = 'https://ytstv.me/episode/young-sheldon-season-2-episode-'
reqs = requests.get(url) #Request the url
soup = BeautifulSoup(reqs.text, 'html.parser')

count = 1
episodeCount = int(input("Episode Count: "))


while count <= episodeCount:
    newurl = url + str(count)
    #webbrowser.open(newurl)

    newreqs = requests.get(newurl)
    newSoup = BeautifulSoup(newreqs.text, "lxml")
    #print(newSoup)

    for thing in newSoup.findAll('a', class_ = 'lnk-lnk lnk-4'): #Just match the lnk number#
        #print(thing)
        #print(str(thing))

        strlist = ""

        for char in str(thing):
            strlist += char

            if char == ">":
                break

        #print(strlist)
        strlist = strlist.replace(">", "")
        strlist = strlist.replace("<a class=", "")
        #strlist = strlist.replace("lnk-lnk lnk-2", "")
        strlist = strlist.replace("lnk-lnk lnk-4", "")
        strlist = strlist.replace(" href=", "")
        strlist = strlist.replace('"', '')

        print(strlist)
        webbrowser.open(strlist)





    time.sleep(1)
    count+=1





