import webbrowser
import time

import requests
from bs4 import BeautifulSoup

url = 'https://www.etsy.com/search?q=aot%20shirt'
reqs = requests.get(url) #Request the url
soup = BeautifulSoup(reqs.text, 'lxml')


count = 0

for thing in soup.findAll('h3', class_ = 'wt-text-caption'):
    count+=1
    print(count)
    holdString = thing.text

    print(thing.text)