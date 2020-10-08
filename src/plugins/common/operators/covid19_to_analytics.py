from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator, SkipMixin


class Covid19ToAnalytics(BaseOperator, SkipMixin):
    @apply_defaults
    def __init__(
            self, *args, **kwargs,
    ):
        super(Covid19ToAnalytics, self).__init__(*args, **kwargs)

    def execute(self, context):
        pg_hook = PostgresHook(postgres_conn_id='postgres-ingestions')
        pg_hook_analytics = PostgresHook(postgres_conn_id='postgres-analytics-dw')
        day = context['ds']
        pg_hook_analytics.run("DELETE FROM covid19_stats where day = %s", parameters=[day])
        sql_read = """SELECT data #>> '{Country}' as country, 
                             (data #>> '{Confirmed}')::int as confirmed,
                             (data #>> '{Deaths}')::int as deaths,
                             (data #>> '{Recovered}')::int as recovered,   
                             (data #>> '{Active}')::int as active,
                             day  
                      FROM covid19 where day =%s"""

        rows = pg_hook.get_records(sql_read, parameters=[day])
        pg_hook_analytics.insert_rows('covid19_stats', rows=rows,
                                      target_fields=['country', 'confirmed', 'deaths', 'recovered', 'active', 'day'])
