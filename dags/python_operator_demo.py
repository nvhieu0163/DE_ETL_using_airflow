from curses import keyname
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'hieunv',
    'retries': 5,
    'retry_delay' : timedelta(minutes=10)
}


def greet(name, age):
    print(f"Hello guys, my name is {name}, I'm {age} years old. ")


def greet_with_another_task_data(ti):
    firstname = ti.xcom_pull(task_ids='get_name', key='first_name')
    lastname = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello guys, my name is {firstname} {lastname}, "
          f"and I'm {age} years old. ")


def get_name(ti):
    ti.xcom_push(key='first_name', value='Hieu')
    ti.xcom_push(key='last_name', value='Nguyen')


def get_age(ti):
    ti.xcom_push(key='age', value=21)


with DAG(
    default_args=default_args,
    dag_id='DAG_with_python_operator',
    description='DAG run with python Operator and sharing data via task using xcoms',
    start_date=datetime(2022, 7, 19),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name': 'Hieunv', 'age' : 21} #keyword arguments
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    task4 = PythonOperator(
        task_id='greet2',
        python_callable=greet_with_another_task_data
    )

    #task dependency
    task1

    [task2, task3] >> task4