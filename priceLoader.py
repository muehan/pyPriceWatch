import requests 
import sys
import re
import urllib3
import json
import math
from models import ProductModel

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

def getProductsFromGraphqlEndpoint(id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Host": "www.digitec.ch",
        "x-dg-mandator": "406802",
        "x-dg-customertype": "standard",
        "x-dg-loginstatus": "loggedOut",
        "x-dg-userid": "null",
        "x-dg-testgroup": "undefined",
        "x-dg-sessionz": "3JWkNj4Ix3NRlVOjdJlKCA==",
        "x-dg-correlation-id": "6ce69274-0f0e-45a9-87f4-644fc9d1b10e",
        "Content-Type": "application/json",
        "x-dg-routename": "productDetail",
        "x-dg-portal": "25",
        "x-dg-buildid": "314293",
        "x-dg-scrumteam": "Isotopes",
        "x-dg-country": "ch"
    }

    totalcount = getTotalCount(id)
    totalRoundedUp = roundup(totalcount)

    productModels = []

    for i in range(0, int(totalRoundedUp / 100)):
        offset = i * 100
        limit = 100

        print('offset: ' + str(offset) + ' limit: ' + str(limit))

        data = '[ '\
	       '{ '\
		        '"operationName":"GET_PRODUCT_TYPE_PRODUCTS_AND_FILTERS", '\
		        '"variables": '\
		        '{'\
		            '"productTypeId":' + str(id) + ','\
			        '"queryString":"",'\
			        '"offset":' + str(offset) + ','\
			        '"limit":' + str(limit) + ','\
			        '"sort":"AVAILABILITY",'\
			        '"siteId":null,'\
			        '"sectorId":1'\
		        '},'\
		        '"extensions":'\
		        '{'\
			        '"persistedQuery":'\
			        '{'\
				       '"version":1,'\
				       '"sha256Hash":"cd2107b20ecd5954254487b28679b7a12d0a42139e5ea1a244fcb281539a6a48"'\
			        '}'\
		        '}'\
	        '}'\
            ']'

        r = requests.post(url = 'https://www.digitec.ch/api/graphql', data = data, headers = headers, verify = False)
        result = json.loads(r.text)
        listObject = result[0]
        data = listObject["data"]
        productType = data["productType"]
        filterProducts = productType["filterProductsV4"]
        products = filterProducts["products"]
        productsResults = products["results"]
        for pr in productsResults:
            try:
                prices = pr["pricing"]
                price = prices["price"]
                if not price:
                    continue
                inkl = price["amountIncl"]

                model = ProductModel(pr["id"], pr["productIdAsString"], pr["name"], pr["fullName"], pr["simpleName"], inkl)
            except (Exception) as error:
                print("unmarshal"  + str(error))
                print(pr)

            productModels.append(model)

    return productModels

def getTotalCount(id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Host": "www.digitec.ch",
        "x-dg-mandator": "406802",
        "x-dg-customertype": "standard",
        "x-dg-loginstatus": "loggedOut",
        "x-dg-userid": "null",
        "x-dg-testgroup": "undefined",
        "x-dg-sessionz": "3JWkNj4Ix3NRlVOjdJlKCA==",
        "x-dg-correlation-id": "6ce69274-0f0e-45a9-87f4-644fc9d1b10e",
        "Content-Type": "application/json",
        "x-dg-routename": "productDetail",
        "x-dg-portal": "25",
        "x-dg-buildid": "314293",
        "x-dg-scrumteam": "Isotopes",
        "x-dg-country": "ch"
    }

    data = '[ '\
	       '{ '\
		        '"operationName":"GET_PRODUCT_TYPE_PRODUCTS_AND_FILTERS", '\
		        '"variables": '\
		        '{'\
		            '"productTypeId":' + str(id) + ','\
			        '"queryString":"",'\
			        '"offset":0,'\
			        '"limit":2000,'\
			        '"sort":"AVAILABILITY",'\
			        '"siteId":null,'\
			        '"sectorId":1'\
		        '},'\
		        '"extensions":'\
		        '{'\
			        '"persistedQuery":'\
			        '{'\
				       '"version":1,'\
				       '"sha256Hash":"cd2107b20ecd5954254487b28679b7a12d0a42139e5ea1a244fcb281539a6a48"'\
			        '}'\
		        '}'\
	        '}'\
            ']'

    r = requests.post(url = 'https://www.digitec.ch/api/graphql', data = data, headers = headers, verify = False)
    result = json.loads(r.text)
    listObject = result[0]
    data = listObject["data"]
    productType = data["productType"]
    filterProducts = productType["filterProductsV4"]
    productCounts = filterProducts["productCounts"]

    return productCounts["total"]

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def getPriceText(content):
    pattern = "<div class=\"productDetail [0-9a-zA-Z]{4}\"><header>\d*</header><div class=\"[0-9a-zA-Z]{4}\">.*<strong[0-9a-zA-Z=\" ]{0,100}> [0-9./–]{4,10}</strong>"
    result = re.findall(pattern, content)

    if not result:
        return "0"
    element = result[0]

    pattern = "[0-9 .–]{4,10}"
    price = re.findall(pattern, element)
    if ".–" in price[0]:
        return price[0][:-2].replace(' ','')
    else:
        return price[0].replace(' ','')

def getPriceTextFromMetaTag(content):
    pattern = r'<meta property="product:price:amount" content="[0-9]{0,5}"/>'
    result = re.findall(pattern, content)

    if not result:
        return getPriceText(content)

    element = result[0]
    pattern = "[0-9]{1,5}"
    price = re.findall(pattern, element)

    return price[0]

def getNameText(content):
    pattern = '<h1 class="productName [a-zA-Z0-9]{4}"><strong>.*</strong>.*</h1>'
    result = re.findall(pattern, content)
    if not result:
        return "no name found"
    
    htmlPattern = r'<[a-zA-Z0-9="/ ]+>'
    htmlEncodedChars = r'&\w+;'
    noHtmlElements = re.sub(htmlPattern, '', result[0]).replace('<!-- -->', '')
    noEncoding = re.sub(htmlEncodedChars, '', noHtmlElements)
    return noEncoding

def call(url):
    content = getContentFor(url)
    price = getPriceText(content)
    name = getNameText(content)
    return price + "," + name


# products = getProductsFromGraphqlEndpoint(83)
# for p in products:
#     print(p.price)