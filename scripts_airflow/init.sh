#!/usr/bin/env bash

# Setup DB Connection String
AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN
DBT_POSTGRESQL_CONN_DEV="postgresql+psycopg2://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:${DBT_POSTGRES_PORT}/${DBT_POSTGRES_DB}_dev"
DBT_POSTGRESQL_CONN_TEST="postgresql+psycopg2://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:${DBT_POSTGRES_PORT}/${DBT_POSTGRES_DB}_test"
AIRFLOW__CORE__FERNET_KEY=mkA0ggJccF5BSlGBIY5adyXAyPqpYizW9KhdJFjgdaQ=
export AIRFLOW__CORE__FERNET_KEY

sleep 20

airflow upgradedb
airflow connections --add --conn_id 'dbt_postgres_instance_raw_data_dev' --conn_uri $DBT_POSTGRESQL_CONN_DEV
airflow connections --add --conn_id 'dbt_postgres_instance_raw_data_test' --conn_uri $DBT_POSTGRESQL_CONN_TEST
airflow connections -a --conn_id covid19-api --conn_type http --conn_host 'https://api.covid19api.com'
airflow variables -i /airflow/resources/dev/all.json
airflow scheduler & airflow webserver
