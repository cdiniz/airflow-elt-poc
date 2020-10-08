from airflow.hooks.http_hook import HttpHook

class Covid19Hook(HttpHook):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self, country="portugal", start_date=None, end_date=None):
        response = self.run(endpoint="/country/{}".format(country),data={"from": start_date + 'T00:00:00Z', "to": end_date  + 'T23:59:59Z'})
        response.raise_for_status()
        return response.json()
