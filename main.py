from storeLink import Store
import priceLoader
import psycopg2
import logger

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
    try:
        store.open()
        ids = store.getProductTypeIds()
        logger.info("loaded all ids")
        for id in ids:
            products = priceLoader.getProductsFromGraphqlEndpoint(id["value"])
            logger.info("loaded all products for: " + str(id))
            logger.info(str(len(products)))

            for product in products:
                # print(product.id + ' - ' + product.name + " - " + str(product.price))
                productid = store.ProductCreateIfNotExist(product, id["key"])
                store.storePrice(productid, product.price, product.insteadOfPrice)

        store.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('main: ' + str(error))
    finally:
        store.close()
