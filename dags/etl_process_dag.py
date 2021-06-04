from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
from etl_process import *
from datetime import datetime, timedelta

import pendulum

local_tz = pendulum.timezone("Asia/Bangkok")

# Update the default arguments and apply them to the DAG.

default_args = {
    'owner': 'phich.bur',
    'start_date': datetime(2021, 6, 4, 16, 2, 0, tzinfo=local_tz),
    'end_date': datetime(2021, 6, 4, 17, 2, 0, tzinfo=local_tz),
    #'email': ['linis94596@geekale.com'],
    #'email_on_failure': False,
    #'email_on_retry': ['linis94596@geekale.com'],
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(dag_id='etl_process', schedule_interval='*/1 * * * *',
          default_args=default_args)


create_tempfiles = BashOperator(task_id='create_tempfiles',
                                bash_command='cd /opt/airflow/dags && mkdir -p iot_temp_data',
                                dag=dag)

extract_from_db = PythonOperator(task_id='extract_from_db',
                                 python_callable=extract_from_db,
                                 dag=dag)

transform_data = PythonOperator(task_id='transform_data',
                                python_callable=transform_data,
                                dag=dag)

load_to_db = PythonOperator(task_id='load_to_db',
                            python_callable=load_to_db,
                            dag=dag)

cleanup_tempfiles = BashOperator(task_id='cleanup_tempfiles',
                                 bash_command='cd /opt/airflow/dags && rm -rf iot_temp_data',
                                 dag=dag)

create_tempfiles >> extract_from_db >> transform_data >> load_to_db >> cleanup_tempfiles
