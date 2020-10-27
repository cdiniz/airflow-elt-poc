from unittest.mock import patch

import pytest
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import TaskInstance
from datetime import datetime

from common.hooks.covid19_hook import Covid19Hook
from common.operators.covid19_to_ingestions import Covid19ToIngestions


class TestCovid19ToIngestionsOperator:
    _pg_hook = PostgresHook(postgres_conn_id='dbt_postgres_instance_raw_data')
    _sql_select = "SELECT * FROM covid19"
    _sql_delete = "DELETE FROM covid19"
    _start_date = datetime.now()

    def setup_method(self):
        self._pg_hook.run(self._sql_delete)

    def teardown_method(self):
        self._pg_hook.run(self._sql_delete)

    _sample_response = [{
        "Country": "Portugal",
        "CountryCode": "PT",
        "Province": "",
        "City": "",
        "CityCode": "",
        "Lat": "39.4",
        "Lon": "-8.22",
        "Confirmed": 72939,
        "Deaths": 1944,
        "Recovered": 47380,
        "Active": 23615,
        "Date": "2020-07-12T00:00:00Z"
    }]

    @pytest.mark.parametrize("test_input,expected",
                             [
                                 (iter([]), 0),
                                 (iter([[]]), 0),
                                 (iter([_sample_response]), 1),
                                 (iter([_sample_response, _sample_response]), 2),
                             ])
    @patch.object(Covid19Hook, 'get_data')
    def test_execute_with_valid_response(self, mock, test_input, expected, dag):
        mock.side_effect = [test_input]
        task = Covid19ToIngestions(dag=dag, task_id="test_task")
        ti = TaskInstance(task=task, execution_date=self._start_date)
        task.execute(ti.get_template_context())
        data = self._pg_hook.get_records("SELECT * FROM covid19")
        assert len(data) == expected
        if expected >= 1:
            assert data[0][1] == self._sample_response[0]
            assert data[0][2] == self._start_date.date()

    @pytest.mark.parametrize("test_input,expected",
                             [(iter([_sample_response]), 1)])
    @patch.object(Covid19Hook, 'get_data')
    def test_execute_deletes_previous_entry(self, mock, test_input, expected, dag):
        self._pg_hook.insert_rows("covid19", [(self._start_date.date(), '{}')], target_fields=['day', 'data'])
        mock.side_effect = [test_input]
        task = Covid19ToIngestions(dag=dag, task_id="test_task")
        ti = TaskInstance(task=task, execution_date=self._start_date)
        task.execute(ti.get_template_context())
        data = self._pg_hook.get_records("SELECT * FROM covid19")
        assert len(data) == expected
        assert data[0][1] == self._sample_response[0]
        assert data[0][2] == self._start_date.date()
