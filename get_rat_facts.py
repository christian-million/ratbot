import requests
from bs4 import BeautifulSoup

# Rat Facts Source
URL = "https://www.automatictrap.com/pages/101-rat-facts"

response = requests.get(URL)
response_text = BeautifulSoup(response.text, "html.parser")

# The main lists are found here
main_div = response_text.find('div', class_='rte')

# The majority of facts are conveniently located in <li> tags
listed_facts = main_div.find_all('li')

# The rest of the facts are in images, with a generic <p> tag
image_facts = main_div.find_all('p', style="text-align: center;")

# Write down the easily formatted facts
with open("ratfacts.txt", 'a') as f:
    for fact in listed_facts:
        next_fact = fact.text.strip()
        print(next_fact, file=f)

# This file is intended to be cleaned manually, copied to `ratfacts.txt`, and subsequently deleted.
with open("to_clean.txt", "a") as f:
    for fact in image_facts:
        print(fact.text.strip(), file=f)
