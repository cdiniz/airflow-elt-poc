from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator, SkipMixin


class Covid19ToAnalytics(BaseOperator, SkipMixin):
    @apply_defaults
    def __init__(
            self, connection_id, *args, **kwargs,
    ):
        self.connection_id = connection_id
        super(Covid19ToAnalytics, self).__init__(*args, **kwargs)

    def execute(self, context):
        pg_hook = PostgresHook(postgres_conn_id=self.connection_id)
        pg_hook_analytics = PostgresHook(postgres_conn_id=self.connection_id)
        day = context['ds']
        pg_hook_analytics.run("DELETE FROM covid19_stats where day = %s", parameters=[day])
        sql_read = """SELECT data #>> '{Country}' as country, 
                             day,
                             sum((data #>> '{Confirmed}')::int) as confirmed,
                             sum((data #>> '{Deaths}')::int) as deaths,
                             sum((data #>> '{Recovered}')::int) as recovered,   
                             sum((data #>> '{Active}')::int) as active
                      FROM covid19 where day =%s
                      GROUP BY country, day"""

        rows = pg_hook.get_records(sql_read, parameters=[day])
        pg_hook_analytics.insert_rows('covid19_stats', rows=rows,
                                      target_fields=['country', 'day', 'confirmed', 'deaths', 'recovered', 'active'])
