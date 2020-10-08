#!/usr/bin/env bash

set -e

airflow connections -d --conn_id postgres-ingestions
airflow connections -d --conn_id postgres-analytics-dw
airflow connections -d --conn_id covid19-api

airflow connections -a --conn_id postgres-ingestions --conn_type postgres --conn_host 'localhost' --conn_schema 'ingestions' --conn_login airflow --conn_port '5432' --conn_password 'airflow'
airflow connections -a --conn_id postgres-analytics-dw --conn_type postgres --conn_host 'localhost' --conn_schema 'analyticsdw' --conn_login airflow --conn_port '5432' --conn_password 'airflow'
airflow connections -a --conn_id covid19-api --conn_type http --conn_host 'https://api.covid19api.com'
