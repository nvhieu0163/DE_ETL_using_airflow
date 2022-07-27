from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

import os
from os.path import isfile, join
import json
import pandas as pd


def get_log_list(ti):
    fjoin = os.path.join
    logs_file_list = []

    for dir, subdirs, files in os.walk('/opt/airflow/data/log_data'):
        logs_file_list.extend([fjoin(dir, f) for f in files])
    
    ti.xcom_push(key='logs_file_list', value=logs_file_list)


def get_songs_list(ti):
    fjoin = os.path.join
    songs_file_list = []

    for dir, subdirs, files in os.walk('/opt/airflow/data/song_data'):
        songs_file_list.extend([fjoin(dir, f) for f in files])
    
    ti.xcom_push(key='songs_file_list', value=songs_file_list)


def convert_json_to_df(ti):
    log_file_list = ti.xcom_pull(task_ids='get_logs_list', key='logs_file_list')
    songs_file_list = ti.xcom_pull(task_ids='get_songs_list', key='songs_file_list')

    df_log = pd.DataFrame()
    df_songs = pd.DataFrame()

    for link in log_file_list:
        data = [json.loads(line) for line in open(link, 'r')]
        df_log = df_log.append(pd.DataFrame(data), ignore_index = True)

    for link in songs_file_list:
        file = open(link, 'r')
        data = json.load(file)
        df_songs = df_songs.append(pd.DataFrame(data, index = [0]), ignore_index = True)

    df_log.to_csv(f'/opt/airflow/staging_data/logs_data.csv', index = False)
    df_songs.to_csv('/opt/airflow/staging_data/songs_data.csv', index = False)


def transform_users_table():
    df_log = pd.read_csv('/opt/airflow/staging_data/logs_data.csv', header=0)

    #get necessary columns
    df_user = df_log[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    #drop duplicate user, unique userID
    df_user.drop_duplicates(subset='userId', inplace=True)

    #drop null value
    df_user = df_user.dropna(axis=0, subset=['userId', 'firstName', 'lastName', 'gender'])

    #store in staging table
    df_user['userId'] = df_user['userId'].astype(int)
    df_user.to_csv('/opt/airflow/staging_data/user_table.csv', index = False)


def transform_songs_table():
    df_songs = pd.read_csv('/opt/airflow/staging_data/songs_data.csv', header=0)

    #get necessary columns
    df_songs = df_songs[['song_id', 'title', 'artist_id', 'year', 'duration']]

    df_songs.drop_duplicates(subset='song_id', inplace=True)

    #store in staging table
    df_songs.to_csv('/opt/airflow/staging_data/song_table.csv', index = False)


def transform_artist_table():
    df_songs = pd.read_csv('/opt/airflow/staging_data/songs_data.csv', header=0)

    #get necessary columns
    df_artist = df_songs[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]

    df_artist.drop_duplicates(subset='artist_id', inplace=True)

    #store in staging table
    df_artist.to_csv('/opt/airflow/staging_data/artist_table.csv', index = False)


def transform_songsplay_table():
    df_log = pd.read_csv('/opt/airflow/staging_data/logs_data.csv', header=0)
    df_songs = pd.read_csv('/opt/airflow/staging_data/songs_data.csv', header=0)

    #get necessary columns
    df_songplays = df_log.loc[df_log['page'] == 'NextSong']
    df_songplays = df_songplays[['ts', 'userId', 'level', 'sessionId', 'location', 'userAgent', 'song']]
    
    df_songsplays2 = df_songs[['song_id', 'artist_id', 'title']]

    #merge
    df_merged = df_songplays.merge(df_songsplays2, left_on='song', right_on='title', how='left')

    #drop column
    df_final = df_merged[['ts', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent']]

    df_final['userId'] = df_final['userId'].astype(int)
    df_final.to_csv('/opt/airflow/staging_data/songplay_table.csv', index=True)


def transform_time_table():
    df_log = pd.read_csv('/opt/airflow/staging_data/logs_data.csv', header = 0)

    #get timestamp
    df_time = df_log[['ts']]

    #drop duplicate
    df_time.drop_duplicates(subset='ts', inplace=True)

    #broken timestamp to specific units
    hour, day, week, month, year, weekday = ([] for i in range(6))

    for ts in df_time['ts']:
        time_object = pd.to_datetime(ts, utc = True, unit = 'ms')
        hour.append(time_object.hour)
        day.append(time_object.day)
        week.append(time_object.week)
        month.append(time_object.month)
        year.append(time_object.year)
        weekday.append(time_object.weekday())
    
    df_time['hour'] = hour
    df_time['day'] = day
    df_time['week'] = week
    df_time['month'] = month
    df_time['year'] = year
    df_time['weekday'] = weekday

    df_time.to_csv('/opt/airflow/staging_data/time_table.csv', index = False)


default_args = {
    'owner': 'hieunv',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


with DAG(
        dag_id='DAG_with_ETL_songs_data',
        default_args=default_args,
        description='DAG with extract data from dataset and build data warehouse',
        start_date=datetime(2022, 7, 26),
        catchup=False,
        schedule_interval='@daily'
) as dag:
    Task1 = PostgresOperator(
        task_id='init',
        postgres_conn_id='postgres_localhost_Song_Datawarehouse',
        sql='''

            DROP TABLE IF EXISTS users;
            DROP TABLE IF EXISTS songs;
            DROP TABLE IF EXISTS artists;
            DROP TABLE IF EXISTS time;
            DROP TABLE IF EXISTS songsplays;

            CREATE TABLE IF NOT EXISTS users (
                user_id     INT             PRIMARY KEY,
                first_name  VARCHAR(255),
                last_name   VARCHAR(255),
                gender      VARCHAR(1)      CHECK (gender = 'M' OR gender = 'F'),
                level       VARCHAR(16)
            );
            
            CREATE TABLE IF NOT EXISTS songs (
                song_id     VARCHAR(18)     PRIMARY KEY,  
                title       VARCHAR(255),
                artist_id   VARCHAR(18),
                year        INT,
                duration    FLOAT
            );
            
            CREATE TABLE IF NOT EXISTS artists (
                artist_id   VARCHAR(18)     PRIMARY KEY,
                name        VARCHAR(255),
                location    VARCHAR(255),
                latitude    FLOAT,
                longitude   FLOAT
            );
            
            CREATE TABLE IF NOT EXISTS time (
                start_time  VARCHAR(13),
                hour        INT     CHECK(hour >=0 AND hour < 24),
                day         INT,
                week        INT,
                month       INT     CHECK (month >= 1 AND month <=12),
                year        INT,
                weekday     VARCHAR(16)
            );
            
            CREATE TABLE IF NOT EXISTS songsplays (
                songplay_id SMALLSERIAL PRIMARY KEY,
                start_time  VARCHAR(13),
                user_id     INT,
                level       VARCHAR(16),
                song_id     VARCHAR(18),
                artist_id   VARCHAR(18),
                session_id  INT,
                location    VARCHAR(255),
                user_agent  TEXT
            );
        '''
    )

    Task2 = PythonOperator(
        task_id='get_logs_list',
        python_callable=get_log_list
    )

    Task3 = PythonOperator(
        task_id='get_songs_list',
        python_callable=get_songs_list
    )

    Task4 = PythonOperator(
        task_id='store_into_stagging_data',
        python_callable=convert_json_to_df
    )

    Task5 = PythonOperator(
        task_id='transform_users_table',
        python_callable=transform_users_table
    )

    Task6 = PythonOperator(
        task_id='transform_songs_table',
        python_callable=transform_songs_table
    )

    Task7 = PythonOperator(
        task_id='transform_artist_table',
        python_callable=transform_artist_table
    )

    Task8 = PythonOperator(
        task_id='transform_time_table',
        python_callable=transform_time_table
    )

    Task9 = PythonOperator(
        task_id='transform_songsplay_table',
        python_callable=transform_songsplay_table
    )


    Task10 = PostgresOperator(
        task_id='load_to_DB',
        postgres_conn_id='postgres_localhost_Song_Datawarehouse',
        sql='''
            COPY users FROM 'X:/Users/nguye/Documents/DataScienceDagoras_mobifone/airflow_docker/staging_data/user_table.csv' DELIMITER ',' CSV HEADER;
            COPY songs FROM 'X:/Users/nguye/Documents/DataScienceDagoras_mobifone/airflow_docker/staging_data/song_table.csv' DELIMITER ',' CSV HEADER; 
            COPY artists FROM 'X:/Users/nguye/Documents/DataScienceDagoras_mobifone/airflow_docker/staging_data/artist_table.csv' DELIMITER ',' CSV HEADER;
            COPY songsplays FROM 'X:/Users/nguye/Documents/DataScienceDagoras_mobifone/airflow_docker/staging_data/songplay_table.csv' DELIMITER ',' CSV HEADER;
            COPY time FROM 'X:/Users/nguye/Documents/DataScienceDagoras_mobifone/airflow_docker/staging_data/time_table.csv' DELIMITER ',' CSV HEADER;
        '''
    )

    
    #dependency
    Task1 >> [Task2, Task3] >> Task4 >> [Task5, Task6, Task7, Task8, Task9] >> Task10
