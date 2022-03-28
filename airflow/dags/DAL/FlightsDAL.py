import sys; import os;

sys.path.insert(1, '/opt/airflow/dags')
import DB.Pg as Pg

def copiarDatos(pDf):
    Pg.copiar(pDf, 'delay')


def verificarExistente(pAño):

    sqlSelect = f"select origin from delay where year = {pAño} limit 1"

    result = Pg.ejecutarQuery(sqlSelect)
    
    if len(result) == 0:
        return False
    else:
        return True
