import requests 
import sys
import re

def getPrice(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, verify = False, headers = headers)
    content = response.text
    
    # <div class="productDetail Z1a6"><header></header><div class="Z1ab"><strong class="ZZon"> 153.–</strong>
    pattern = "<div class=\"productDetail [0-9a-zA-Z]{4}\"><header></header><div class=\"[0-9a-zA-Z]{4}\"><strong class=\"[0-9a-zA-Z]{4}\"> [0-9]{1,10}.–</strong>"

    result = re.findall(pattern, content)


    if result:
        print("Search successful.")
        print(result)
    else:
        print("Search unsuccessful.")	

URL = sys.argv[1]
getPrice(URL)