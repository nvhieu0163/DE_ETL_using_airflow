from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'hieunv',
    'retries': 5,
    'retry_delay' : timedelta(minutes=60)
}

'''
Co 2 cach de co the set scheduler interval:
    - timedelta, cac python package time
    - Su dung Cron Expression: Co the kiem tra tai link: https://crontab.guru/
'''

with DAG(
    dag_id='DAG_with_cron_expression',
    default_args=default_args,
    start_date=datetime(2022, 7, 7, 10),
    catchup=True, #True: running from start date to schedule_interval (incase start_date < current_date)
    schedule_interval='0 9,12 * * 2-5', #running at 9am and 12pm from Tuesday to Friday in every week, Timezone = UTC
    dagrun_timeout=timedelta(minutes=60) 
) as dag:
    Task1 = BashOperator(
        task_id='Print_date_dag_runs',
        bash_command='echo "{{ ds }}" && sleep 1'
    )

    Task1