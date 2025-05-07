import os
import time
from pathlib import Path

from bs4 import BeautifulSoup

import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup

url = "https://www.vlr.gg/team/2593/fnatic"

request_result = requests.get(url)  # Request the url
soup = BeautifulSoup(request_result.text, 'html.parser')

print(soup)

team_summary_soup = soup.findAll('div', class_='team-summary-container-1')
print(team_summary_soup)
print(len(team_summary_soup))


a_in_team_summary_soup = team_summary_soup[0].findAll('a', class_='wf-card fc-flex m-item')

print(len(a_in_team_summary_soup))

upcoming_soup = soup.find('span', class_='rm-item-score-eta')
print(upcoming_soup.text)


# general upcoming page

url = "https://www.vlr.gg/matches"

request_result = requests.get(url)  # Request the url
soup = BeautifulSoup(request_result.text, 'html.parser')


def has_exact_class(tag):
    return (
        tag.name == 'div' and
        tag.has_attr('class') and
        tag['class'] == ['wf-card']
    )



wf_card_soup = soup.findAll(has_exact_class)

print(len(wf_card_soup))



for entry in wf_card_soup:
    print(entry)
    print("\n\n\n\n")
    time.sleep(5)