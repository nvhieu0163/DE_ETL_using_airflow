from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import sqlite3
import os
import pandas as pd


dag_path = os.getcwd() + '/airflow'
    

def transform(ti):
    booking_df = pd.read_csv(f"{dag_path}/raw_data/booking.csv", low_memory=False)
    client_df = pd.read_csv(f"{dag_path}/raw_data/client.csv", low_memory=False)
    hotel_df = pd.read_csv(f"{dag_path}/raw_data/hotel.csv", low_memory=False)

    #merging booking with client
    data = pd.merge(booking_df, client_df, on='client_id')
    data.rename(columns={'name' : 'client_name', 'type' : 'client_type'}, inplace=True)

    #merging with hotel
    data = pd.merge(data, hotel_df, on='hotel_id')
    data.rename(columns={'name' : 'hotel_name'}, inplace=True)

    #reformat the date
    data.booking_date = pd.to_datetime(data.booking_date, infer_datetime_format=True)

    #make all cost in GBP currency
    data.loc[data.currency == 'EUR', ['booking_cost']] = data.booking_cost * 0.8
    data.currency.replace("EUR", "GBP", inplace=True)

    #drop address column
    data = data.drop('address', 1)

    #load to csv
    data.to_csv(f"{dag_path}/processed_data/processed_data.csv", index=False)


def load():
    conn = sqlite3.connect(f"{dag_path}/db/ETL_example.db")
    c = conn.cursor()
    c.execute('''
                CREATE TABLE IF NOT EXISTS booking_record (
                    client_id       INTEGER     NOT NULL,
                    booking_date    TEXT        NOT NULL,
                    room_type       TEXT(512)   NOT NULL,
                    hotel_id        INTEGER     NOT NULL,
                    booking_cost    NUMERIC,
                    currency        TEXT,
                    age             INTEGER,
                    client_name     TEXT(512),
                    client_type     TEXT(512),
                    hotel_name      TEXT(512)
                );
             ''')
    records = pd.read_csv(f"{dag_path}/airflow/processed_data/processed_data.csv")
    records.to_sql('booking_record', conn, if_exists='replace', index=False)


default_args={
    'owner': 'hieunv',
    'retries' : 5,
    'retry_delay' :timedelta(minutes=10)
}


with DAG(
    dag_id='DAG_with_ETL_local_DB',
    default_args=default_args,
    description='DAG with extract data from a local file, transform and extract to DB',
    start_date=datetime(2022, 7, 20, 7),
    catchup=False,
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='Transform_data',
        python_callable=transform
    )

    task2 = PythonOperator(
        task_id='Load_data',
        python_callable=load
    )

    task1 >> task2 