import webbrowser
import time

import requests
from bs4 import BeautifulSoup

url = 'https://www.midiworld.com/handel.htm' #Can be changed as long as it is in the same website
reqs = requests.get(url) #Request the url
soup = BeautifulSoup(reqs.text, 'html.parser')

MIDIList = [] #Stores the detected MIDI files from the website
for link in soup.find_all('a'):
    print(link.get('href')) #Show all urls in the site
    if str(link.get('href')).endswith('mid'): #Performs the detection
        MIDIList.append(link.get('href'))

print(MIDIList)
print(len(MIDIList))

for entry in MIDIList:
    webbrowser.open(entry)
    time.sleep(1)