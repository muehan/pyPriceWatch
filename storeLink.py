import psycopg2
import datetime
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

    def getProductTypeIds(self):
        ids = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM producttype")
            rows = cur.fetchall()

            for row in rows:
                id = row[0]
                typeid = row[1]
                ids.append({"key": id, "value": typeid})

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return ids

    def storePrice(self, id, price, insteadOfPrice):

        if not id:
            print('No Id defined for price')
            return

        try:
            now = datetime.datetime.now()
            dateStr = '' + str(now.year) + '-' + \
                str(now.month).zfill(2) + '-' + str(now.day).zfill(2)

            curs = self.conn.cursor()

            curs.execute(
                "SELECT * FROM price where productId = '{0}' and date = '{1}'".format(id, dateStr))
            row = curs.fetchone()

            if not row:
                cur = self.conn.cursor()
                cur.execute(
                    "INSERT INTO price (productid, price, insteadOfPrice) VALUES(%s, %s, %s)", (id, price, insteadOfPrice))
                self.conn.commit()
                cur.close()

            curs.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def addProduct(self, url, name):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO product (url, name) VALUES(%s, %s) RETURNING id;", (url, name))
            id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()

            print('product created: ' + id)

            return id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def addProductName(self, url, name):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE product set name = %s where url =%s;", (name, url))
            self.conn.commit()
            cur.close()

            print('product updated: ' + name)

            return id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def addProductType(self, typeid, name):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO producttype (typeid, name) VALUES(%s, %s) RETURNING id;", (typeid, name))
            id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()

            print('producttype created: ' + id)

            return id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def ProductCreateIfNotExist(self, product, productTypeId):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM product where productId = '{0}'".format(product.id))
            row = cur.fetchone()

            if not row:
                curc = self.conn.cursor()
                curc.execute("""
                    INSERT INTO product 
                    (producttypeid, productId, productIdAsString, name, fullname, simpleName) 
                    VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;""", (productTypeId, product.id, product.productIdAsString, product.name, product.fullname, product.simpleName))
                id = curc.fetchone()[0]
                self.conn.commit()
                curc.close()
            else:
                id = row[0]

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return id

    def close(self):
        self.conn.close()
