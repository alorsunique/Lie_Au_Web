from selenium import webdriver
from selenium.webdriver.common.by import By


# URL of the website
website_url = "https://embrace-autism.com/raads-r/?fbclid=IwAR1P88laRttRiTHzyYS-lZxdStS6iya_-XoQn10JA4BGKH_UyXb2i4o1F_Q#test"

print(f"Loading Edge")
driver = webdriver.Firefox()

print(f"Opening Website")

# Open the website
driver.get(website_url)

print(f"Loading element")
div_element = driver.find_elements(By.CSS_SELECTOR,'.psychometrics-items-container.item-1')
print(type(div_element))
print(f"Element Found")

print(div_element)
# Get the inner HTML of the div element
for entry in div_element:

    sub_element = entry.find_elements(By.CLASS_NAME,'psychometrics-option-radio')

    print(type(sub_element))
    print(sub_element)
    print(len(sub_element))

    sub_element[0].click()