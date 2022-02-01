#!/bin/bash

echo "Downloading 'GlobalLandTemperaturesByCity.csv'..............................."

curl -L -o /tmp/dump.zip "https://www.dropbox.com/s/j63tkpiwbjsup2l/GlobalLandTemperaturesByCity.zip?dl=0"

unzip /tmp/dump.zip GlobalLandTemperaturesByCity.csv -d /tmp