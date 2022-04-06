import psycopg2
import pandas as pd
from io import StringIO 
import csv

userDatabase = 'postgres'
passwordDatabase ='KBJZTtjrmPXr'
hostDatabase = 'database-1.chvryskzgbbb.us-east-1.rds.amazonaws.com'
portDatabase = '5432'
database = 'postgres'



def ejecutarQuery(pQuery, pDatabase = None):

    _connStr = 'postgresql://'+userDatabase+':'+passwordDatabase+'@'+hostDatabase+':'+portDatabase+'/'+database

    conn = psycopg2.connect(_connStr)
    with conn:
        return pd.read_sql(pQuery,conn)

def ejecutarTransformacion(pQuery, pDatabase = None):

    _connStr = 'postgresql://'+userDatabase+':'+passwordDatabase+'@'+hostDatabase+':'+portDatabase+'/'+database

    conn = psycopg2.connect(_connStr)
    cursor = conn.cursor()
    cursor.execute(pQuery)

    conn.commit()
    count = cursor.rowcount
    print(f"Transformation - {count} rows affected")
    return

def forzarEjecucion(pQuery, pDatabase = None):
    _connStr = 'postgresql://'+userDatabase+':'+passwordDatabase+'@'+hostDatabase+':'+portDatabase+'/'+database

    conn = psycopg2.connect(_connStr)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(pQuery)

    conn.commit()
    print(f"Delete / Create")
    return

def copiar(pDataframe, pNombreTabla):

    _connStr = 'postgresql://'+userDatabase+':'+passwordDatabase+'@'+hostDatabase+':'+portDatabase+'/'+ database
    conn = psycopg2.connect(_connStr)

    sio = StringIO()
    sio.write(pDataframe.to_csv(sep="|",index=None, header=None))
    
    sio.seek(0) 
    # print(sio.getvalue())
    
    with conn.cursor() as c:
        c.copy_from(sio, pNombreTabla, columns=pDataframe.columns.str.lower(), sep='|', null='')
        conn.commit()
        count = c.rowcount
        print(f"Copy - {count} rows affected")