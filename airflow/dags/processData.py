# Imports del Script
import time
import os

# Cosas de Airflow
from datetime import datetime, timedelta
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

import BLL.DoCalcs as DoCalcs

args={
    'owner': 'axel',
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
    DoCalcs.calculateDelay(kwargs['year'])

with dag:

    procesar_2009 = PythonOperator(
        task_id = 'procesar_2009',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2009'}
    )
    
    procesar_2010 = PythonOperator(
        task_id = 'procesar_2010',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2010'}
    )

    procesar_2011 = PythonOperator(
        task_id = 'procesar_2011',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2011'}
    )

    procesar_2012 = PythonOperator(
        task_id = 'procesar_2012',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2012'}
    )

    procesar_2013 = PythonOperator(
        task_id = 'procesar_2013',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2013'}
    )

    procesar_2014 = PythonOperator(
        task_id = 'procesar_2014',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2014'}
    )

    procesar_2015 = PythonOperator(
        task_id = 'procesar_2015',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2015'}
    )

    procesar_2016 = PythonOperator(
        task_id = 'procesar_2016',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2016'}
    )

    procesar_2017 = PythonOperator(
        task_id = 'procesar_2017',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2017'}
    )

    procesar_2018 = PythonOperator(
        task_id = 'procesar_2018',
        python_callable=_proceso,
        provide_context=True,
        op_kwargs={'year': '2018'}
    )

    procesar_2009 >> procesar_2010 >> procesar_2011 >> procesar_2012 >> procesar_2013 >> procesar_2014 >> procesar_2015 >> procesar_2016 >> procesar_2017 >> procesar_2018