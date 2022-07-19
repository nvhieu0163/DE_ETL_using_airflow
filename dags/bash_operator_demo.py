from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_agruments = {
    'owner': 'hieunv',
    'retries': 5,
    'retry_delay' : timedelta(minutes=60)
}

with DAG(
    dag_id='bash_operator_demo',
    default_args=default_agruments,
    description='This is first DAG',
    start_date=datetime(2022, 7, 19, 14),
    schedule_interval='@daily'

) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo "Hello World", this is the first task!'
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo This is the second task!'
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo This is the third task!'
    )

    task1 >> [task2, task3]