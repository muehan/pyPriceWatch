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
    print(totalcount)

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
            '"query":'\
            '"query GET_PRODUCT_TYPE_PRODUCTS_AND_FILTERS(  $productTypeId: Int!  $queryString: String!  $offset: Int  $limit: Int  $sort: ProductSort  $siteId: String  $sectorId: Int  $withDefaultOffer: Boolean) {  productType(id: $productTypeId) {    filterProductsV4(      queryString: $queryString      offset: $offset      limit: $limit      sort: $sort      siteId: $siteId      sectorId: $sectorId      withDefaultOffer: $withDefaultOffer    ) {      productCounts {        total        filteredTotal        __typename      }      products {        hasMore        results {          ...Product          __typename        }        resultsWithDefaultOffer {          ...ProductWithOffer          __typename        }        __typename      }      __typename    }    __typename  }}fragment Product on Product {  id  productIdAsString  productTypeIdAsString  productTypeName  imageUrl  imageSet {    alternateText    source    __typename  }  sectorId  name  brandId  brandName  fullName  simpleName  nameProperties  productConditionLabel  marketingDescription  pricing {    supplierId    secondHandSalesOfferId    price {      ...VatMoney      __typename    }    priceRebateFraction    insteadOfPrice {      type      price {        ...VatMoneySum        __typename      }      __typename    }    volumeDiscountPrices {      minAmount      price {        ...VatMoneySum        __typename      }      isDefault      __typename    }    __typename  }  availability {    icon    mail {      siteId      title      type      icon      text      description      tooltipDescription      deliveryDate      __typename    }    pickup {      title      notAllowedText      description      isAllowed      __typename    }    pickMup {      description      isAllowed      __typename    }    sites {      siteId      title      type      icon      text      description      tooltipDescription      deliveryDate      __typename    }    isFloorDeliveryAllowed    __typename  }  energyEfficiency {    energyEfficiencyColorType    energyEfficiencyLabelText    energyEfficiencyLabelSigns    energyEfficiencyImageUrl    __typename  }  salesInformation {    numberOfItems    numberOfItemsSold    isLowAmountRemaining    __typename  }  showroomSites  rating  totalRatings  totalQuestions  isIncentiveCashback  incentiveText  isNew  isBestseller  isProductSet  isSalesPromotion  isComparable  isDeleted  isHidden  canAddToBasket  hidePrice  germanNames {    germanProductTypeName    nameWithoutProperties    germanProductNameProperties    germanNameWithBrand    __typename  }  productGroups {    productGroup1    productGroup2    productGroup3    productGroup4    __typename  }  isOtherMandatorProduct  __typename}fragment ProductWithOffer on ProductWithOffer {  mandatorSpecificData {    ...ProductMandatorSpecific    __typename  }  product {    ...ProductMandatorIndependent    __typename  }  offer {    ...ProductOffer    __typename  }  __typename}fragment VatMoney on VatMoney {  amountIncl  amountExcl  fraction  currency  __typename}fragment VatMoneySum on VatMoneySum {  amountIncl  amountExcl  currency  __typename}fragment ProductMandatorSpecific on MandatorSpecificData {  isBestseller  isDeleted  showroomSites  sectorIds  __typename}fragment ProductMandatorIndependent on ProductV2 {  id  productId  name  nameProperties  productTypeId  productTypeName  brandId  brandName  averageRating  totalRatings  totalQuestions  isProductSet  images {    url    height    width    __typename  }  energyEfficiency {    energyEfficiencyColorType    energyEfficiencyLabelText    energyEfficiencyLabelSigns    energyEfficiencyImage {      url      height      width      __typename    }    __typename  }  hasVariants  smallDimensions  __typename}fragment ProductOffer on OfferV2 {  id  productId  offerId  shopOfferId  price {    amountIncl    amountExcl    currency    fraction    __typename  }  supplier {    name    countryIsoCode    countryName    deliversFromAbroad    __typename  }  label  type  volumeDiscountPrices {    minAmount    price {      amountIncl      amountExcl      currency      __typename    }    isDefault    __typename  }  salesInformation {    numberOfItems    numberOfItemsSold    isEndingSoon    __typename  }  incentiveText  isIncentiveCashback  isNew  isSalesPromotion  hideInProductDiscovery  canAddToBasket  hidePrice  insteadOfPrice {    type    price {      amountIncl      amountExcl      currency      fraction      __typename    }    __typename  }  __typename}"'\
            '}'\
            ']'
        try:
            # print(data + "\n\n")
            r = requests.post(url='https://www.digitec.ch/api/graphql',
                          data=data, headers=getHeaders(), verify=False)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logger.error('error' + e.response)
            raise SystemExit(e)
        result = json.loads(r.text)
        if not result:
            return productModels
        listObject = result[0]
        if not listObject["data"]:
            print("there is an error in the api resonse")
            continue
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
        '"query":'\
        '"query GET_PRODUCT_TYPE_PRODUCTS_AND_FILTERS(  $productTypeId: Int!  $queryString: String!  $offset: Int  $limit: Int  $sort: ProductSort  $siteId: String  $sectorId: Int  $withDefaultOffer: Boolean) {  productType(id: $productTypeId) {    filterProductsV4(      queryString: $queryString      offset: $offset      limit: $limit      sort: $sort      siteId: $siteId      sectorId: $sectorId      withDefaultOffer: $withDefaultOffer    ) {      productCounts {        total        filteredTotal        __typename      }      products {        hasMore        results {          ...Product          __typename        }        resultsWithDefaultOffer {          ...ProductWithOffer          __typename        }        __typename      }      __typename    }    __typename  }}fragment Product on Product {  id  productIdAsString  productTypeIdAsString  productTypeName  imageUrl  imageSet {    alternateText    source    __typename  }  sectorId  name  brandId  brandName  fullName  simpleName  nameProperties  productConditionLabel  marketingDescription  pricing {    supplierId    secondHandSalesOfferId    price {      ...VatMoney      __typename    }    priceRebateFraction    insteadOfPrice {      type      price {        ...VatMoneySum        __typename      }      __typename    }    volumeDiscountPrices {      minAmount      price {        ...VatMoneySum        __typename      }      isDefault      __typename    }    __typename  }  availability {    icon    mail {      siteId      title      type      icon      text      description      tooltipDescription      deliveryDate      __typename    }    pickup {      title      notAllowedText      description      isAllowed      __typename    }    pickMup {      description      isAllowed      __typename    }    sites {      siteId      title      type      icon      text      description      tooltipDescription      deliveryDate      __typename    }    isFloorDeliveryAllowed    __typename  }  energyEfficiency {    energyEfficiencyColorType    energyEfficiencyLabelText    energyEfficiencyLabelSigns    energyEfficiencyImageUrl    __typename  }  salesInformation {    numberOfItems    numberOfItemsSold    isLowAmountRemaining    __typename  }  showroomSites  rating  totalRatings  totalQuestions  isIncentiveCashback  incentiveText  isNew  isBestseller  isProductSet  isSalesPromotion  isComparable  isDeleted  isHidden  canAddToBasket  hidePrice  germanNames {    germanProductTypeName    nameWithoutProperties    germanProductNameProperties    germanNameWithBrand    __typename  }  productGroups {    productGroup1    productGroup2    productGroup3    productGroup4    __typename  }  isOtherMandatorProduct  __typename}fragment ProductWithOffer on ProductWithOffer {  mandatorSpecificData {    ...ProductMandatorSpecific    __typename  }  product {    ...ProductMandatorIndependent    __typename  }  offer {    ...ProductOffer    __typename  }  __typename}fragment VatMoney on VatMoney {  amountIncl  amountExcl  fraction  currency  __typename}fragment VatMoneySum on VatMoneySum {  amountIncl  amountExcl  currency  __typename}fragment ProductMandatorSpecific on MandatorSpecificData {  isBestseller  isDeleted  showroomSites  sectorIds  __typename}fragment ProductMandatorIndependent on ProductV2 {  id  productId  name  nameProperties  productTypeId  productTypeName  brandId  brandName  averageRating  totalRatings  totalQuestions  isProductSet  images {    url    height    width    __typename  }  energyEfficiency {    energyEfficiencyColorType    energyEfficiencyLabelText    energyEfficiencyLabelSigns    energyEfficiencyImage {      url      height      width      __typename    }    __typename  }  hasVariants  smallDimensions  __typename}fragment ProductOffer on OfferV2 {  id  productId  offerId  shopOfferId  price {    amountIncl    amountExcl    currency    fraction    __typename  }  supplier {    name    countryIsoCode    countryName    deliversFromAbroad    __typename  }  label  type  volumeDiscountPrices {    minAmount    price {      amountIncl      amountExcl      currency      __typename    }    isDefault    __typename  }  salesInformation {    numberOfItems    numberOfItemsSold    isEndingSoon    __typename  }  incentiveText  isIncentiveCashback  isNew  isSalesPromotion  hideInProductDiscovery  canAddToBasket  hidePrice  insteadOfPrice {    type    price {      amountIncl      amountExcl      currency      fraction      __typename    }    __typename  }  __typename}"'\
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
