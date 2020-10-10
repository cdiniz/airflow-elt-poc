from unittest.mock import patch

import pytest
from airflow.hooks.http_hook import HttpHook

from plugins.common.hooks.covid19_hook import Covid19Hook
from tests.plugins.common.utils.mock_response import MockResponse

sample_data_pt = [ {
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
    }
]

sample_data_gb = [ {
        "Country": "Gibraltar",
        "CountryCode": "GI",
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
    }
]

sample_countries_data =[
  {
    "Country": "Portugal",
    "Slug": "portugal",
    "ISO2": "PT"
  },
  {
    "Country": "Gibraltar",
    "Slug": "gibraltar",
    "ISO2": "GI"
  }
]


@pytest.mark.parametrize("test_input,expected",
                         [
                             ([[], []], []),
                             ([list(filter(lambda x: x['Country'] == 'Portugal',sample_countries_data)), sample_data_pt], [sample_data_pt]),
                             ([sample_countries_data, sample_data_pt, sample_data_gb], [sample_data_pt, sample_data_gb])
                         ])
@patch.object(HttpHook, 'run')
def test_get_data_valid_responses(mock, test_input, expected, dag):
    mock.side_effect = list(map(lambda x: MockResponse(x, 200),test_input))
    hook = Covid19Hook()
    data = list(hook.get_data(start_date='2020-07-12', end_date='2020-07-12'))
    if len(test_input) > 0:
        mock.assert_any_call(endpoint="/countries")
        for country in list(map(lambda x: x['Slug'], test_input[0])):
            mock.assert_any_call(data={"from": '2020-07-12T00:00:00Z', "to": '2020-07-12T23:59:59Z'},
                            endpoint="/country/{}".format(country))
    assert data == expected


@patch.object(HttpHook, 'run')
def test_execute_invalid_status_code(mock, dag):
    with pytest.raises(Exception) as excinfo:
        mock.side_effect = [MockResponse({}, 404)]
        hook = Covid19Hook()
        list(hook.get_data(start_date='2020-07-12', end_date='2020-07-13'))
    assert "error code" in str(excinfo.value)