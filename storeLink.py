import psycopg2
from config import config
 
def connect():
    urls = []
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM url")
        rows = cur.fetchall()

        for row in rows:
            id = row[0]
            url = row[1]
            urls.append({"key": id, "value": url})
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return urls

def storePrice(url, price):
    conn = None
    try:
        params = config()
 
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

 
if __name__ == '__main__':
    connect()