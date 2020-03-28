import storeLink
import priceLoader

# with open('list.txt') as f:
#     line = f.readline()
#     cnt = 1
#     while line:
#         # print(line)
#         price = priceLoader.call(line)
#         print(price)
#         print("")
#         line = f.readline()

def getUrls():
    return storeLink.connect()

if __name__ == '__main__':
    urls = getUrls()
    for url in urls:
        content = priceLoader.getContentFor(url)
        price = priceLoader.getPriceText(content)
        name = priceLoader.getNameText(content)
        print(price)
        print(name)