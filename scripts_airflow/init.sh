#!/usr/bin/env bash

# Setup DB Connection String
AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN
DBT_POSTGRESQL_CONN="postgresql+psycopg2://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:${DBT_POSTGRES_PORT}/${DBT_POSTGRES_DB}"
AIRFLOW__CORE__FERNET_KEY=mkA0ggJccF5BSlGBIY5adyXAyPqpYizW9KhdJFjgdaQ=
export AIRFLOW__CORE__FERNET_KEY

sleep 20

airflow upgradedb
airflow connections --add --conn_id 'dbt_postgres_instance_raw_data' --conn_uri $DBT_POSTGRESQL_CONN
airflow connections -a --conn_id covid19-api --conn_type http --conn_host 'https://api.covid19api.com'
airflow variables -i /airflow/resources/dev/all.json
airflow scheduler & airflow webserver
