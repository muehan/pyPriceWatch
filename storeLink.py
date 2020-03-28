import psycopg2
from config import config
 
def connect():
    urls = []
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
   # execute a statement
        print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)

        cur.execute("SELECT * FROM url")
        rows = cur.fetchall()

        for row in rows:
            url = row[1]
            urls.append(url)
       
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return urls
 
if __name__ == '__main__':
    connect()