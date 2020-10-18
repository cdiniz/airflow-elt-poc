from airflow.hooks.http_hook import HttpHook
import time

class Covid19Hook(HttpHook):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self, start_date=None, end_date=None, rate_limit=0.5):
        response = self.run(endpoint="/countries")
        response.raise_for_status()
        countries = list(map(lambda x: x['Slug'], response.json()))
        for country in countries:
            response = self.run(endpoint="/country/{}".format(country),data={"from": start_date + 'T00:00:00Z', "to": end_date  + 'T23:59:59Z'})
            time.sleep(rate_limit)
            response.raise_for_status()
            yield response.json()

