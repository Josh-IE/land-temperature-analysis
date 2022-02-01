#!/bin/bash
set -e

#!/bin/bash

echo "Downloading 'GlobalLandTemperaturesByCity.csv'..............................."

curl -L -o /tmp/dump.zip "https://www.dropbox.com/s/j63tkpiwbjsup2l/GlobalLandTemperaturesByCity.zip?dl=0"

unzip /tmp/dump.zip GlobalLandTemperaturesByCity.csv -d /tmp

echo "Copying 'GlobalLandTemperaturesByCity.csv' to 'Global_Land_Temperatures_By_City'..............................."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    \c planetly;
    COPY "Global_Land_Temperatures_By_City"
        FROM '/tmp/GlobalLandTemperaturesByCity.csv'
        DELIMITER ','
        CSV HEADER;
EOSQL

echo "'GlobalLandTemperaturesByCity.csv' successfully copied to 'Global_Land_Temperatures_By_City'"