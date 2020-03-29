from storeLink import Store
import priceLoader
import psycopg2

# with open('list.txt') as f:
#     line = f.readline()
#     cnt = 1
#     while line:
#         # print(line)
#         price = priceLoader.call(line)
#         print(price)
#         print("")
#         line = f.readline()

# def getUrls():
#     return storeLink.connect

if __name__ == '__main__':
    store = Store()
    urls = store.getUrls()
    try:
        store.open()
        for url in urls:
            content = priceLoader.getContentFor(url['value'])
            price = priceLoader.getPriceText(content)
            # name = priceLoader.getNameText(content)
            store.storePrice(url['key'], price)
            print(price)
            # print(name)
        store.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        store.close()
    