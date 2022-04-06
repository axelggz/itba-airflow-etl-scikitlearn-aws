# Imports del Script
import time
import os

# Cosas de Airflow
from datetime import datetime, timedelta
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

#import BLL.DoCalcs as DoCalcs

args={
    'owner': 'nacho',
}

dt = datetime.strptime('19 Aug 2021', '%d %b %Y')
newdatetime = dt.replace(hour=14, minute=50)

dag = dag.DAG(
    default_args=args,
    dag_id='processData',
    start_date= datetime(year=2021, month=8, day=19),
    schedule_interval=None,
    description='',
    catchup=False)

def _proceso(**kwargs):
    #DoCalcs.calculateDelay(kwargs['year'])
    print('a')
    # print(numpy.__file__)

with dag:

    procesar_2009 = PythonOperator(
        task_id = 'procesar_2009',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2009'}
    )