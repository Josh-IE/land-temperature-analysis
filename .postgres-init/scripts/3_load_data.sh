#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \c planetly;
    COPY "Global_Land_Temperatures_By_City"
        FROM '/tmp/GlobalLandTemperaturesByCity.csv'
        DELIMITER ','
        CSV HEADER;
EOSQL