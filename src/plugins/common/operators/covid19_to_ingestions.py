from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator, SkipMixin
import json

from common.hooks.covid19_hook import Covid19Hook


class Covid19ToIngestions(BaseOperator, SkipMixin):
    @apply_defaults
    def __init__(
        self,  *args, **kwargs
    ):
        super(Covid19ToIngestions, self).__init__(*args, **kwargs)

    def execute(self, context):
        pg_hook = PostgresHook(postgres_conn_id='postgres-ingestions')
        api_hook = Covid19Hook(http_conn_id='covid19-api', method='GET')
        pg_hook.run("DELETE FROM covid19 where day = %s", parameters=[context['ds']])
        for country_data in api_hook.get_data(start_date=context['ds'],end_date=context['ds']):
            for entry in country_data:
                pg_hook.run("INSERT INTO covid19(data,day) VALUES(%s,%s)", parameters=(json.dumps(entry), context['ds']))



