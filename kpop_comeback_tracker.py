# For tracking K POP comebacks
# Data taken from kpopofficial.com

import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def track(url):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    try:
        day_content_soup = soup.findAll('figure', class_='wp-block-table is-style-stripes')

        for day_content in day_content_soup:
            body_content_soup = day_content.findAll('tbody')
            tr_content_soup = body_content_soup[0].findAll('tr')

            for tr_content in tr_content_soup:

                date = ""
                time = ""
                artist = ""

                td_element = tr_content.findAll('td', class_='has-text-align-right')

                for element in td_element:
                    content = element.get_text(separator=' ').strip()
                    date_split = content.split("at")

                    try:
                        date = date_split[0].strip()
                    except IndexError:
                        pass

                    try:
                        time = date_split[1].strip()
                    except IndexError:
                        pass

                td_element = tr_content.findAll('td', class_='has-text-align-left')

                for element in td_element:
                    try:
                        artist = element.find('strong').get_text(separator=' ').strip()

                        for strong_tag in element.find_all('strong'):
                            strong_tag.decompose()  # Removes the <strong> tag and its contents

                        content_list = list(element.stripped_strings)
                    except:
                        pass

                if not date == "" and not artist == "":
                    try:
                        print(f"{date} | {time} | {artist} | {content_list}")
                    except:
                        pass

    except:
        pass


if __name__ == "__main__":

    # Get the current month and year
    datetime_object = datetime.fromtimestamp(time.time())

    current_month = datetime_object.month
    current_year = datetime_object.year

    month_map = {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december"
    }

    formatted_url = f"https://kpopofficial.com/kpop-comeback-schedule-{month_map[current_month]}-{current_year}/"
    track(formatted_url)
