from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
import json

from common.operators.covid19_to_analytics import Covid19ToAnalytics
from common.operators.covid19_to_ingestions import Covid19ToIngestions

default_args = json.loads(Variable.get('covid19'))
default_args.update({"retry_delay":  timedelta(minutes=default_args["retry_delay"])})

with DAG(dag_id="covid19", default_args=default_args, schedule_interval="@daily") as dag:
    ingest_covid19_day_task = Covid19ToIngestions(task_id='ingest_covid19_day', provide_context=True, dag=dag)
    transform_and_load_covid19_day_task = Covid19ToAnalytics(task_id='transform_covid19_day', provide_context=True, dag=dag)
    ingest_covid19_day_task >> transform_and_load_covid19_day_task
