#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE planetly;
    \c planetly;
    CREATE TABLE "Global_Land_Temperatures_By_City" (
        dt date,
        AverageTemperature decimal(30, 28),
        AverageTemperatureUncertainty decimal(30, 28),
        City varchar(255),
        Country varchar(255),
        Latitude varchar(255),
        Longitude varchar(255)
    );
EOSQL