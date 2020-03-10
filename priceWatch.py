import requests 
import sys
from io import StringIO
from lxml import etree

parser = etree.HTMLParser()

def getPrice(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, verify = False, headers = headers)
    content = response.text
    tree = etree.parse(StringIO(content), parser=parser)
    # print(content)
    startIndex = content.find("<strong class=\"ZZdf\">")
    print(f"start: {startIndex}")
    price = content[startIndex:startIndex+35]

    return price

URL = sys.argv[1]
price = getPrice(URL)
print(price)