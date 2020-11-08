# Set these env vars so that:
# 1. airflow commands locally are run against the docker postgres
# 2. `airflow test` runs properly

AIRFLOW_HOME=$(pwd)/airflow

# Note: env vars set here should be printed out in the print statement below
export AIRFLOW_HOME
export AIRFLOW__CORE__EXECUTOR=SequentialExecutor
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflowuser:pssd@localhost:5432/airflowdb
export AIRFLOW__CORE__FERNET_KEY=mkA0ggJccF5BSlGBIY5adyXAyPqpYizW9KhdJFjgdaQ=
export AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/src/dags
export AIRFLOW__CORE__BASE_LOG_FOLDER=$AIRFLOW_HOME/logs
export AIRFLOW__CORE__DAG_PROCESSOR_MANAGER_LOG_LOCATION=$AIRFLOW_HOME/logs/dag_processor_manager/dag_processor_manager.log
export AIRFLOW__SCHEDULER__CHILD_PROCESS_LOG_DIRECTORY=$AIRFLOW_HOME/logs/scheduler

export DBT_DIR=$(pwd)/dbt
export DBT_PROFILES_DIR=$(pwd)/dbt/ci_profiles
export DBT_PROFILE_HOST=localhost
export DBT_PROFILE_USER=user
export DBT_PROFILE_PASSWORD=pass
export DBT_PROFILE_PORT=5433
export DBT_PROFILE_SCHEMA=public
export DBT_PROFILE_DB=covid19_dev
export DBT_PROFILE_DB_TEST=covid19_test


print \
"===================================================================
Environment Variables for Local Execution (vs execution in Docker)
===================================================================
AIRFLOW_HOME=$AIRFLOW_HOME;AIRFLOW__CORE__EXECUTOR=$AIRFLOW__CORE__EXECUTOR;AIRFLOW__CORE__SQL_ALCHEMY_CONN=$AIRFLOW__CORE__SQL_ALCHEMY_CONN;AIRFLOW__CORE__FERNET_KEY=$AIRFLOW__CORE__FERNET_KEY;AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW__CORE__DAGS_FOLDER;AIRFLOW__CORE__PLUGINS_FOLDER=$AIRFLOW__CORE__PLUGINS_FOLDER;AIRFLOW__CORE__BASE_LOG_FOLDER=$AIRFLOW__CORE__BASE_LOG_FOLDER;AIRFLOW__CORE__DAG_PROCESSOR_MANAGER_LOG_LOCATION=$AIRFLOW__CORE__DAG_PROCESSOR_MANAGER_LOG_LOCATION;AIRFLOW__SCHEDULER__CHILD_PROCESS_LOG_DIRECTORY=$AIRFLOW__SCHEDULER__CHILD_PROCESS_LOG_DIRECTORY;DBT_PROFILE_HOST=$DBT_PROFILE_HOST;DBT_PROFILE_USER=$DBT_PROFILE_USER;DBT_PROFILE_PASSWORD=$DBT_PROFILE_PASSWORD;DBT_PROFILE_PORT=$DBT_PROFILE_PORT;DBT_PROFILE_SCHEMA=$DBT_PROFILE_SCHEMA;DBT_PROFILE_DB=$DBT_PROFILE_DB;"
