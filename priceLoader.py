import requests 
import sys
import re
import urllib3

urllib3.disable_warnings()

def getContentFor(url):
    url = url.replace("\n", "")
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, verify = False, headers = headers)
    content = response.text
    content = content.replace('\r', ' ').replace('\n', '').replace('\t', '')

    return content

def getPriceText(content):
    pattern = "<div class=\"productDetail [0-9a-zA-Z]{4}\"><header>\d*</header><div class=\"[0-9a-zA-Z]{4}\">.*<strong[0-9a-zA-Z=\" ]{0,100}> [0-9./–]{4,10}</strong>"
    result = re.findall(pattern, content)

    if not result:
        return "0"
    element = result[0]    

    pattern = "[0-9 .–]{4,10}"
    price = re.findall(pattern, element)
    if ".–" in price[0]:
        return price[0][:-2]
    else:
        return price[0]

def getNameText(content):
    return "test"

def call(url):
    content = getContentFor(url)
    price = getPriceText(content)
    name = getNameText(content)
    return price + "," + name
