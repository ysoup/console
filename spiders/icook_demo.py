# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from bs4 import BeautifulSoup
import re


headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
    }
response = requests.get("https://icook.tw/categories", headers=headers)
soup = BeautifulSoup(response.text, "lxml")
all_info = soup.select("div.entries.accordion-list.mega-menu")[1].find_all("a", "list-title")
all_categories = []
for x in all_info:
    all_categories.append(x["href"].split("/")[-1])
    print(x["href"])
print(all_categories)