from airflow import DAG
from datetime import datetime, timedelta

from airflow.models import Variable
from airflow.settings import json
from airflow_dbt.operators.dbt_operator import (
    DbtRunOperator,
    DbtTestOperator
)
import os

from common.operators.covid19_to_ingestions import Covid19ToIngestions

default_args = json.loads(Variable.get('covid19'))
default_args.update({"retry_delay":  timedelta(minutes=default_args["retry_delay"])})


dbt_dir = os.environ["DBT_DIR"]
dbt_profiles_dir = os.environ["DBT_PROFILES_DIR"]

with DAG( 'covid19_dbt',
    default_args=default_args,
    description='Managing dbt data pipeline',
    schedule_interval='@daily') as dag:

    ingest_covid19_day_task = Covid19ToIngestions(task_id='ingest_covid19_day_to_dbt', dag=dag)

    dbt_run = DbtRunOperator(
        task_id='dbt_run',
        dir = dbt_dir,
        profiles_dir=dbt_profiles_dir
    )

    dbt_test = DbtTestOperator(
        task_id='dbt_test',
        dir=dbt_dir,
        profiles_dir=dbt_profiles_dir,
        retries=0  # Failing tests would fail the task, and we don't want Airflow to try again
    )

    ingest_covid19_day_task >> dbt_run >> dbt_test
