from storeLink import Store
import priceLoader
import psycopg2
import sys

def add(url):
    store = Store()
    store.open()
    try:
        store.open()
        content = priceLoader.getContentFor(url)
        name = priceLoader.getNameText(content)

        store.addProductName(url, name)
        
        store.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        store.close()

if __name__ == '__main__':
    url = sys.argv[1]
    add(url)