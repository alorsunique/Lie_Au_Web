# This script should automate answering the RAADS-R test

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set the answer key here
# The test has 80 questions and an array will dictate what answer will be chosen for each question
answer_tile_element = []
count = 64
down_count = count
while down_count > 0:
    answer_tile_element.append(0)
    down_count -=1
down_count = count
while down_count > 0:
    answer_tile_element.append(3)
    down_count -=1
print(f"Answer Tile\n{answer_tile_element}")

answer_key = np.tile(np.array(answer_tile_element),80)
print(f"Answer Key\n{answer_key}")

# Open browser
print(f"Loading Browser")
driver = webdriver.Firefox()

# Open the website
website_url = "https://embrace-autism.com/raads-r/?fbclid=IwAR1P88laRttRiTHzyYS-lZxdStS6iya_-XoQn10JA4BGKH_UyXb2i4o1F_Q#test"
print(f"Opening Website")
driver.get(website_url)

div_element_list = []

# Stores all the div elements for the questions
count = 0
while count < 80:
    count += 1
    div_element = driver.find_elements(By.CSS_SELECTOR, f'.psychometrics-items-container.item-{count}')
    div_element_list += div_element

# Answers the questions here
count = 0
for element in div_element_list:
    sub_element = element.find_elements(By.CLASS_NAME, 'psychometrics-option-radio')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    sub_element[int(answer_key[count])].click()
    count += 1
