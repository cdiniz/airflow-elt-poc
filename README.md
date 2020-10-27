## This repo is a POC of Airflow and DBT for ELT pipelines on a CI environment. 
The goal is a personal evaluation of Airflow and Dbt, exploring the following topics:
 - Setup airflow for a ci environment, how to develop and execute locally.
 - Implement custom operators/hooks, etc.
 - Testing Airflow dags, operators, hooks, using a TDD Approach.
 - Reusability of custom components.
 - Error handling in pipelines
 - ELT Comparison between airflow and airflow+dbt.
 - Testing DBT (besides dbt testing),
 for instance: testing if a view has the information that should.
 - How Dbt handles incremental views

### The simple data pipeline example:
Read data from https://covid19api.com/, stage the data on a covid19 table, 
and transform the data into covid19_stats which has the stats per day per country. 

#### Install local dev environment

Install virtual env

`pip install virtualenv
`

Create env

`virtualenv .venv
`

Activate env

`source .venv/bin/activate
`

Install the same requirements as the docker image

`pip install -r requirements-docker.txt
`

Install requirements for development

`pip install -r requirements-dev.txt`

#### Init docker

`docker-compose up`

#### Init Environment 
##### Local development, testing and airflow local execution

`source dev-env.sh
`

#### Test

`python -m pytest`

#### Run backfills

`airflow backfill covid19_dbt -s 2020-10-02 -e 2020-10-02
`

`airflow backfill covid19 -s 2020-10-02 -e 2020-10-02
`
#### Test Dag Tasks

`airflow test covid19_dbt dbt_run 2020-10-02
`

`airflow test covid19_dbt dbt_test 2020-10-02
`
