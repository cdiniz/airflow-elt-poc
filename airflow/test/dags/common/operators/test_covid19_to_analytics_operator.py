import json

import pytest
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import TaskInstance
import datetime

from common.operators.covid19_to_analytics import Covid19ToAnalytics


class TestCovid19ToAnalyticsOperator:

    def setup_method(self):
        self._pg_hook.run(self._sql_delete_analytics)
        self._pg_hook.run(self._sql_delete_ingestions)

    def teardown_method(self):
        self._pg_hook.run(self._sql_delete_analytics)
        self._pg_hook.run(self._sql_delete_ingestions)


    _pg_hook = PostgresHook(postgres_conn_id='dbt_postgres_instance_raw_data_test')
    _sql_select = "SELECT country, confirmed, deaths, recovered, active, day FROM covid19_stats"
    _sql_delete_analytics = "DELETE FROM covid19_stats"
    _sql_delete_ingestions = "DELETE FROM covid19"
    _start_date = datetime.datetime.now()

    _sample_data = {
        "Country": "Portugal",
        "Confirmed": 72939,
        "Deaths": 1944,
        "Recovered": 47380,
        "Active": 23615
    }

    _sample_data_analytics = ("Portugal",
                              72939,
                              1944,
                              47380,
                              23615,
                              _start_date.date())

    _sample_data_analytics_grouped = ("Portugal",
                              72939*2,
                              1944*2,
                              47380*2,
                              23615*2,
                              _start_date.date())


    @pytest.mark.parametrize("test_input,expected",
                             [
                                 ([], [0, []]),
                                 ([_sample_data],[1, [_sample_data_analytics]]),
                                 ([_sample_data,_sample_data], [1, [_sample_data_analytics_grouped]])
                             ])
    def test_execute(self, test_input, expected, dag):
        if len(test_input) > 0:
            data = list(map(lambda x: (json.dumps(x), self._start_date), test_input))
            self._pg_hook.insert_rows('covid19', data, target_fields=['data', 'day'])
        task = Covid19ToAnalytics(dag=dag, task_id="test_task", connection_id='dbt_postgres_instance_raw_data_test')
        ti = TaskInstance(task=task, execution_date=self._start_date)
        task.execute(ti.get_template_context())

        data = self._pg_hook.get_records(self._sql_select)

        assert len(data) == expected[0]
        assert data == expected[1]


    @pytest.mark.parametrize("test_input,expected",
                             [
                                 ([_sample_data], [1,  [_sample_data_analytics]])
                             ])
    def test_execute_delete_previous_entry(self, test_input, expected, dag):
        data = list(map(lambda x: (json.dumps(x), self._start_date), test_input))
        self._pg_hook.insert_rows('covid19', data, target_fields=['data', 'day'])
        self._pg_hook.insert_rows("covid19_stats", [(self._start_date.date(),"Portugal")], target_fields=['day', 'country'])
        task = Covid19ToAnalytics(dag=dag, task_id="test_task", connection_id='dbt_postgres_instance_raw_data_test')
        ti = TaskInstance(task=task, execution_date=self._start_date)
        task.execute(ti.get_template_context())

        data = self._pg_hook.get_records(self._sql_select)

        assert len(data) == expected[0]
        assert data == expected[1]
