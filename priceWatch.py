import requests 
import sys
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if(tag == 'div'):
            if "class=\"productDetail" in attrs:
                print("attribute: ", attrs)

    def handle_endtag(self, tag):
        b = tag
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        b = data
        # print("Encountered some data  :", data)

parser = MyHTMLParser()

def getPrice(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, verify = False, headers = headers)
    content = response.text
    parser.feed(content)
    # print(content)
    startIndex = content.find("<strong class=\"ZZcy\">")
    print(f"start: {startIndex}")
    price = content[startIndex:startIndex+35]

    return price



URL = sys.argv[1]
price = getPrice(URL)
print(price)