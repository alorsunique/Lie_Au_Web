import webbrowser
import time

import requests
from bs4 import BeautifulSoup

url = 'https://ytstv.me/episode/house-of-the-dragon-season-1-episode-'
reqs = requests.get(url) #Request the url
soup = BeautifulSoup(reqs.text, 'html.parser')


count = 1
episodeCount = int(input("Episode Count: "))

finalList = []

def strList(thing):
    strlist = ""

    for char in str(thing):
        strlist += char

        if char == ">":
            break

    # print(strlist)


    strlist = strlist.replace(">", "")
    strlist = strlist.replace("<a class=", "")
    strlist = strlist.replace("lnk-lnk lnk-2", "")
    strlist = strlist.replace("lnk-lnk lnk-4", "")
    strlist = strlist.replace("lnk-lnk lnk-1", "")
    strlist = strlist.replace("lnk-lnk lnk-3", "")
    strlist = strlist.replace(" href=", "")
    strlist = strlist.replace('"', '')


    return(strlist)


while count <= episodeCount:
    #print("Enter")
    print(count)
    newurl = url + str(count)
    #webbrowser.open(newurl)

    newreqs = requests.get(newurl)
    newSoup = BeautifulSoup(newreqs.text, "lxml")
    #print(newSoup)

    finalURL = ""

    for thing in newSoup.findAll('a', class_ = 'lnk-lnk lnk-1'): #Just match the lnk number#
        #print(thing)
        #print(str(thing))


        aaaaa = strList(thing)
        #print(aaaaa)

        if not aaaaa.find("(1080p).torrent") == -1:
            #print("A1")
            finalURL = aaaaa

    for thing in newSoup.findAll('a', class_ = 'lnk-lnk lnk-2'): #Just match the lnk number#
        #print(thing)
        #print(str(thing))


        aaaaa = strList(thing)
        #(aaaaa)

        if not aaaaa.find("(1080p).torrent") == -1:
            #print("A2")
            finalURL = aaaaa

    for thing in newSoup.findAll('a', class_ = 'lnk-lnk lnk-3'): #Just match the lnk number#
        #print(thing)
        #print(str(thing))


        aaaaa = strList(thing)
        #print(aaaaa)


        if not aaaaa.find("(1080p).torrent") == -1:
            #print("A3")
            finalURL = aaaaa

    for thing in newSoup.findAll('a', class_ = 'lnk-lnk lnk-4'): #Just match the lnk number#
        #print(thing)
        #print(str(thing))


        aaaaa = strList(thing)
        #print(aaaaa)

        if not aaaaa.find("(1080p).torrent") == -1:
            #print("A4")
            finalURL = aaaaa

    print(finalURL)
    finalList.append(finalURL)
    #webbrowser.open(finalURL)


    count+=1

print(finalList)


for entry in finalList:
    webbrowser.open(entry)





