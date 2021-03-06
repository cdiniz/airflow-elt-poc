from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator, SkipMixin
import json

from common.hooks.covid19_hook import Covid19Hook


class Covid19ToIngestions(BaseOperator, SkipMixin):
    @apply_defaults
    def __init__(
        self,  connection_id, *args, **kwargs
    ):
        self.connection_id = connection_id
        super(Covid19ToIngestions, self).__init__(*args, **kwargs)

    def execute(self, context):
        pg_hook = PostgresHook(postgres_conn_id=self.connection_id)
        api_hook = Covid19Hook(http_conn_id='covid19-api', method='GET')
        pg_hook.run("DELETE FROM covid19 where day = %s", parameters=[context['ds']])
        rows = map(lambda x: (json.dumps(x[0]), context['ds']),filter(lambda x: len(x), api_hook.get_data(start_date=context['ds'],end_date=context['ds'])))
        pg_hook.insert_rows("covid19",rows,["data","day"])



