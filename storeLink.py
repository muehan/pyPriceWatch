import psycopg2
from config import config

class Store:
        
    conn = None

    def open(self):
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def getUrls(self):
        urls = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()

            for row in rows:
                id = row[0]
                url = row[1]
                urls.append({"key": id, "value": url})
        
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return urls

    def storePrice(self, id, price):

        if not id:
            print('No Id defined for price')
            return

        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO price (productid, price) VALUES(%s, %s)", (id, price))
            self.conn.commit()
            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def addProduct(self, url, name):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO product (url, name) VALUES(%s, %s) RETURNING id;", (url, name))
            id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()

            print('product created: ' + id)

            return id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        self.conn.close()
