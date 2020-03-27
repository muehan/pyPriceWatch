import requests 
import sys
import re
import urllib3

def getPriceElement(url):
    url = url.replace("\n", "")
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, verify = False, headers = headers)
    content = response.text
    content = content.replace('\r', ' ').replace('\n', '').replace('\t', '')

    # print(content)
    
    # <div class="productDetail Z1a6"><header></header><div class="Z1ab"><strong class="ZZon"> 153.–</strong>
    # pattern = "<div class=\"productDetail [0-9a-zA-Z]{4}\"><header></header><div class=\"[0-9a-zA-Z]{4}\"><strong class=\"[0-9a-zA-Z]{4}\"> [0-9./–]{4,10}</strong>"
    # pattern = "<div class=\"productDetail [0-9a-zA-Z]{4}\">.*<strong[0-9a-zA-Z=\\ ]{0,100}> [0-9./–]{4,10}</strong>"
    pattern = "<div class=\"productDetail [0-9a-zA-Z]{4}\"><header>\d*</header><div class=\"[0-9a-zA-Z]{4}\">.*<strong[0-9a-zA-Z=\" ]{0,100}> [0-9./–]{4,10}</strong>"

    # current regex state
    #<div class=\"productDetail [0-9a-zA-Z]{4}\"><header>\d*</header><div class=\"[0-9a-zA-Z]{4}\">.*<strong[0-9a-zA-Z=" ]{0,100}> [0-9./–]{4,10}</strong>

    result = re.findall(pattern, content)

    if result:
        # print("Search successful.")
        return result[0]
    else:
        # print("Search unsuccessful.")
        return ""

def getPriceText(element):
    if not element:
        print(element)
        return "no price found"

    pattern = "[0-9 .–]{4,10}"
    price = re.findall(pattern, element)
    if ".–" in price[0]:
        return price[0][:-2]
    else:
        return price[0]

def call(url):
    element = getPriceElement(url)
    price = getPriceText(element)
    return price

urllib3.disable_warnings()

# URL = sys.argv[1]
# element = getPriceElement(URL)
# price = getPriceText(element)
# print(price)

# demo data
# <div class="productDetail Z18k"><header></header><div class="Z18p"><strong class="ZZe2"> 157.–</strong>

# <div class="productDetail Z18h"><header></header><div class="Z18m"><strong class="ZZda"> 99.20</strong></div>

# <div class="productDetail Z18h"><header><div class="ZZha"><div class="ZZpf ZZpg">–13%</div></div></header><div class="Z18m"><span class="ZZda ZZd8"><strong> 271.–</strong><span class="appendix ZZd9">statt <!-- --> 310.–</span></span></div>