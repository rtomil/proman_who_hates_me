import psycopg2
from psycopg2 import extras
import os
import urllib


def excute_sql(query, data=None, method="all", is_dict=False):
    '''
    Create connection with DB and executes sql queries.
    '''
    conn = None
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except psycopg2.OperationalError as error:
        print("Uh oh.. something went wrong!")
        print(error)
    else:
        conn.autocommit = True
        if is_dict is False:
            with conn.cursor() as cursor:
                cursor.execute(query, data) if data else cursor.execute(query)
                if method == "column":
                    return [row[0] for row in cursor]
                elif method == "one":
                    return cursor.fetchone()[0]
                elif method == "all":
                    return cursor.fetchall()
        elif is_dict:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, data) if data else cursor.execute(query)
                if method == 'one':
                    return cursor.fetchone()
                elif method == 'all':
                    return cursor.fetchall()

    finally:
        if conn:
            conn.close()
