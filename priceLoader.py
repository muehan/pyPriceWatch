import requests
import sys
import re
import urllib3
import json
import math
import logger
from models import ProductModel

urllib3.disable_warnings()

def getContentFor(url):
    url = url.replace("\n", "")
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, verify=False, headers=headers)
    content = response.text
    content = content.replace('\r', ' ').replace('\n', '').replace('\t', '')

    return content


def getProductsFromGraphqlEndpoint(id):
    logger.info("loading all products for: " + str(id))

    totalcount = getTotalCount(id)
    totalRoundedUp = roundup(totalcount)

    productModels = []

    for i in range(0, int(totalRoundedUp / 100)):
        offset = i * 100
        limit = 100

        logger.info('offset: ' + str(offset) + ' limit: ' + str(limit))

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
            '"sha256Hash":"822e1996a25a7fd6d1d31c854a08f2707fad924139eca0342ffd2c537d3bebc5"'\
            '}'\
            '}'\
            '}'\
            ']'
        try:
            r = requests.post(url='https://www.digitec.ch/api/graphql',
                          data=data, headers=getHeaders(), verify=False)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logger.error('error' + e.response)
            raise SystemExit(e)
        result = json.loads(r.text)
        listObject = result[0]
        data = listObject["data"]
        productType = data["productType"]
        filterProducts = productType["filterProductsV4"]
        products = filterProducts["products"]
        productsResults = products["results"]

        # NORMAL PRICE
        # "pricing": {
        #     "supplierId": null,
        #     "secondHandSalesOfferId": null,
        #     "price": {
        #         "amountIncl": 389,
        #         "amountExcl": 361.19,
        #         "fraction": 0.077,
        #         "currency": "CHF",
        #         "__typename": "VatMoney"
        #     },
        #     "priceRebateFraction": null,
        #     "insteadOfPrice": null,
        #     "volumeDiscountPrices": [],
        #     "__typename": "Pricing"
        # },

        # Reduced Price
        # "pricing": {
        #     "supplierId": null,
        #     "secondHandSalesOfferId": null,
        #     "price": {
        #         "amountIncl": 339,
        #         "amountExcl": 314.76,
        #         "fraction": 0.077,
        #         "currency": "CHF",
        #         "__typename": "VatMoney"
        #     },
        #     "priceRebateFraction": 0.12,
        #     "insteadOfPrice": {
        #         "type": "SALESPRICEBEFORE",
        #         "price": {
        #             "amountIncl": 384,
        #             "amountExcl": 356.55,
        #             "currency": "CHF",
        #             "__typename": "VatMoneySum"
        #         },
        #         "__typename": "InsteadOfPrice"
        #     },

        for pr in productsResults:
            try:
                pricing = pr["pricing"]
                price = pricing["price"]
                if not price:
                    continue
                inkl = price["amountIncl"]

                insteadOfPrice = findInseadOfPrice(pricing)

                model = ProductModel(pr["id"], pr["productIdAsString"], pr["name"],
                                     pr["fullName"], pr["simpleName"], inkl, insteadOfPrice)

            except (Exception) as error:
                print("unmarshal" + str(error))
                print(pr)
                logger.error('error' + str(error))

            productModels.append(model)

    return productModels


def findInseadOfPrice(pricing):
    insteadOfPrice = pricing["insteadOfPrice"]

    if insteadOfPrice is not None:
        price = insteadOfPrice["price"]
        insteadOfInkl = price["amountIncl"]
        return insteadOfInkl
    
    return None


def getTotalCount(id):

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
        '"sha256Hash":"5e95c793d5baba15ad5788c6706f5f06d8633a7daccc15d0172fe76827bbc26b"'\
        '}'\
        '}'\
        '}'\
        ']'

    r = requests.post(url='https://www.digitec.ch/api/graphql',
                      data=data, headers=getHeaders(), verify=False)
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
        return price[0][:-2].replace(' ', '')
    else:
        return price[0].replace(' ', '')


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

def getHeaders():
     return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Host": "www.digitec.ch",
        # "x-dg-mandator": "406802",
        # "x-dg-customertype": "standard",
        # "x-dg-loginstatus": "loggedOut",
        # "x-dg-userid": "null",
        # "x-dg-testgroup": "undefined",
        # "x-dg-sessionz": "3JWkNj4Ix3NRlVOjdJlKCA==",
        # "x-dg-correlation-id": "6ce69274-0f0e-45a9-87f4-644fc9d1b10e",
        "Content-Type": "application/json",
        # "x-dg-routename": "productDetail",
        # "x-dg-portal": "25",
        # "x-dg-buildid": "314293",
        # "x-dg-scrumteam": "Isotopes",
        # "x-dg-country": "ch"
    }

# products = getProductsFromGraphqlEndpoint(83)
# for p in products:
#     print(p.price)
