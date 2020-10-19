## This repo is a proof of concept for a personal evaluation of airflow. 
The goals are understanding the following topics:
 - how easy airflow is for local development
 - how easy airflow is to test and possibly use it in a tdd way
 - how easy is to implement custom operators/hooks, etc
 - how reusable are the custom implemented parts
 - how easy is to integrate great expectations
### Run

```
pip install virtualenv

virtualenv .venv

source .venv/bin/activate

pip install -r requirements-airflow.txt

pip install -r requirements-dev.txt

docker-compose -f docker/docker-compose.yml up
```

### configure testing in pycharm

create project

choose existing interpretor and choose python3.7 from the created .venv

choose from existing sources when prompted

get env vars from 'source env.sh'

mark src as Sources Root

under configurations under python integrated tools, choose pytest as the default test runner

run pytests in tests..
