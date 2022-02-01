#!/bin/bash
set -e

echo "Copying 'GlobalLandTemperaturesByCity.csv' to 'Global_Land_Temperatures_By_City'..............................."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --host localhost --port "$PORT" <<-EOSQL
    \c planetly;
    COPY "Global_Land_Temperatures_By_City"
        FROM '/tmp/GlobalLandTemperaturesByCity.csv'
        DELIMITER ','
        CSV HEADER;
EOSQL

echo "'GlobalLandTemperaturesByCity.csv' successfully copied to 'Global_Land_Temperatures_By_City'"