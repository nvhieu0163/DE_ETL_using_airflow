from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args={
    'owner': 'hieunv',
    'retries' : 5,
    'retry_delay' :timedelta(minutes=10)
}


with DAG(
    dag_id='DAG_with_conn_to_postgres_DB_v02',
    default_args=default_args,
    description='DAG with connect and insert data into DB',
    start_date=datetime(2022, 7, 21),
    catchup=False,
    schedule_interval='@daily'
) as dag:

    task1 = PostgresOperator(
        task_id='create_table_in_PostgresDB',
        postgres_conn_id='postgres_localhost_database1',
        sql='''
            CREATE TABLE IF NOT EXISTS table1 (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        '''
    )

    task2 = PostgresOperator(
        task_id='insert_value_to_table',
        postgres_conn_id='postgres_localhost_database1',
        sql='''
            INSERT INTO table1 (dt, dag_id) VALUES ('{{ ds }}', '{{ dag.dag_id }}')
        '''
    )

    task1 >> task2