from unittest.mock import patch

import pytest
from airflow.hooks.http_hook import HttpHook

from plugins.common.hooks.covid19_hook import Covid19Hook
from tests.plugins.common.utils.mock_response import MockResponse

sample_data = [ {
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
                             ([], []),
                             ([sample_data], [sample_data]),
                         ])
@patch.object(HttpHook, 'run')
def test_execute_valid_responses(mock, test_input, expected, dag):
    mock.side_effect = [MockResponse(test_input, 200)]
    hook = Covid19Hook()
    data = hook.get_data(start_date='2020-07-12', end_date='2020-07-12')
    mock.assert_called_with(data={"from":'2020-07-12T00:00:00Z', "to":'2020-07-12T23:59:59Z'},endpoint="/country/portugal")
    assert data == expected


@patch.object(HttpHook, 'run')
def test_execute_invalid_status_code(mock, dag):
    with pytest.raises(Exception) as excinfo:
        mock.side_effect = [MockResponse({}, 404)]
        hook = Covid19Hook()
        hook.get_data(start_date='2020-07-12', end_date='2020-07-13')
    assert "error code" in str(excinfo.value)
