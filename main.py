from storeLink import Store
import priceLoader
import psycopg2
import logger
import reporting

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

            # reporting.write('product id: ' + str(id) - total: ' + str(len(products)))

            for product in products:
                # print(product.id + ' - ' + product.name + " - " + str(product.price))
                productid = store.ProductCreateIfNotExist(product, id["key"])

                if not store.findPrice(productid):
                    # reporting.write('new price for: \'' + str(productid) + '\'')

                    store.storePrice(
                        productid,
                        product.price,
                        product.insteadOfPrice)

        store.close()
        # reporting.close()
    except (Exception) as error:
        logger.error('main: ' + str(error))
    finally:
        store.close()
