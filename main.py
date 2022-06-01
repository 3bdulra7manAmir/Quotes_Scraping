import requests
from bs4 import BeautifulSoup
import pandas as pd

quotes = []
authors = []
tags = []

web_URL = requests.get("https://quotes.toscrape.com/")

result = web_URL.content

soup = BeautifulSoup(result, "lxml")

quote = soup.find_all("span", {"class": "text"})
author = soup.find_all("small", {"class": "author"})
tag = soup.find_all("meta", {"class": "keywords"})

for i in range(len(quote)):
    quotes.append(quote[i].text)
    authors.append(author[i].text)
    tags.append((tag[i]["content"]))

Data = [quotes, authors, tags]

df = pd.DataFrame({"Quotes": quotes, "Author": authors, "Tags": tags})
df.to_csv('C:/Users/Abdulrahman Amir/Desktop/Extracted.csv')
