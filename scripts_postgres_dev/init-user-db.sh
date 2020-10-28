#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${POSTGRES_DB}" <<-EOSQL

CREATE TABLE covid19_stats
      (ID SERIAL PRIMARY KEY NOT NULL,
       country text NOT NULL,
       deaths INT,
       recovered INT,
       confirmed INT,
       active INT,
       day date,
       created_at timestamp without time zone default now(),
       updated_at timestamp without time zone default now()
       );
CREATE TABLE IF NOT EXISTS covid19
      (ID SERIAL PRIMARY KEY     NOT NULL,
       data jsonb,
       day date NOT NULL,
       created_at timestamp without time zone default now()
);
CREATE DATABASE "$POSTGRES_DB_TEST";
EOSQL


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB_TEST" <<-EOSQL

CREATE TABLE covid19_stats
      (ID SERIAL PRIMARY KEY NOT NULL,
       country text NOT NULL,
       deaths INT,
       recovered INT,
       confirmed INT,
       active INT,
       day date,
       created_at timestamp without time zone default now(),
       updated_at timestamp without time zone default now()
       );
CREATE TABLE IF NOT EXISTS covid19
      (ID SERIAL PRIMARY KEY     NOT NULL,
       data jsonb,
       day date NOT NULL,
       created_at timestamp without time zone default now()
);
EOSQL