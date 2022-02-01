
## SETUP

- Checkout the project
    ```
    git clone https://github.com/Josh-IE/land-temperature-analysis.git
    ```
- Change into repository directory
    ```
    cd land-temperature-analysis
    ```
- Start the database and backend api services
    ```
    docker-compose up
    ```
    Wait for the log message `database system is ready to accept connections` on the terminal.
- Copy the `GlobalLandTemperaturesByCity.csv` to the `Global_Land_Temperatures_By_City` table.
    OIn a different terminal run:
    ```
    PGPASSWORD=postgres POSTGRES_USER=postgres POSTGRES_DB=postgres PORT=8500 ./load_data.sh
    ```
    It would take **a long while**. Wait for the message `'GlobalLandTemperaturesByCity.csv' successfully copied to 'Global_Land_Temperatures_By_City'`.

The api is accessible at http://127.0.0.1:8080/docs

The database can be connected to, by running:
```
PGPASSWORD=postgres psql -h localhost -U postgres -p 8500 -d planetly
```

The api documentation is available at: http://127.0.0.1:8080/docs



## Design choices

The backend service was built using fast api, a fast and powerful python web framework.

**Database**

Postgresql is used as the database. There are 2 scripts that run during the database setup that creates the database, the table and downloads the `GlobalLandTemperaturesByCity.csv` file.

**Top N cities that have the highest monthly AverageTemperature**

**Ordering**

To get the top N cities, we order by both descending order of the AverageTemperature and ascending order of city. This means, if we have the following on the database:


| City | AverageTemperature |
|------|----------------|
| Berlin | 30 |
| Potsdam | 29.5 |
| Potsdam | 29 |
| Cologne | 28 |
| Milan   | 28 |
| Athens  | 28 |


A query for the top 3 cities would return:
| City | AverageTemperature |
|------|----------------|
| Berlin | 30 |
| Potsdam | 29.5 |
| Athens | 28 |

We can see that though, there is a tie between Cologne, Milan and Athens, Athens is selected first, because it comes before the others in the ascending alphabetical order.

Also, Potsdam appears only once, because the endpoint returns unique cities.

**Time range**

The endpoint requires a time range. The start date is required and the end date is optional and defaults to the current date.

**Update an existing entry by specifying a date and a city name**

An assumption is established that no 2 records will have the same date and city.

**Frontend consideration**

The list of temperature records returned are paginated to avoid sending large volumes of data over the network to frontend clients.


## Development time

I spent 8 hours working on the Data ingestion scripts and api endpoints part of the solution.

## Comments/Challenges

Due to the limited time I had for development, the project lacks a number of best practices highlighted:
- Tests: Unit tests for the usecases and integration tests for the endpoints
- Logging 
- Docstrings: To provide description of functions and classes
- Type Annotations
- Commits: The project is one giant commit, this makes it difficult to review the development stages.
- Naming conventions: The column names on the csv file are used on the database and the response fields. Some of these names are not descriptive and do not follow best practices in naming convention. e.g `dt` column on the csv should have been mapped to a `date` column on the database.
- Index table: The `dt` and `city` columns of the database table can be indexed to achieve faster retrieval of record to be updated.

## Examples

**Find the entry whose city has the highest AverageTemperature since the year 2000.**

**Request**

```
curl --location --request GET 'http://127.0.0.1:8080/v1/temperatures/highest?start_date=2000-01-01&limit=1'
```

**Response**

``` json
{
    "items": [
        {
            "dt": "2013-07-01",
            "averagetemperature": 39.15600000000001,
            "averagetemperatureuncertainty": 0.37,
            "city": "Ahvaz",
            "country": "Iran",
            "latitude": "31.35N",
            "longitude": "49.01E"
        }
    ],
    "total": 1,
    "page": 1,
    "size": 50
}
```

**Following above: assume the temperature observation of the city last month breaks the record. It is 0.1 degree higher with the same uncertainty. Create this entry.**

**Request**

``` curl
curl --location --request POST 'http://127.0.0.1:8080/v1/temperatures' \
--header 'Content-Type: application/json' \
--data-raw '{
    "dt": "2022-01-01",
    "averagetemperature": 39.25600000000001,
    "averagetemperatureuncertainty": 0.37,
    "city": "Ahvaz",
    "country": "Iran",
    "latitude": "31.35N",
    "longitude": "49.01E"
}'
```

**Response**

``` json
{
    "dt": "2022-01-01",
    "averagetemperature": 39.25600000000001,
    "averagetemperatureuncertainty": 0.37,
    "city": "Ahvaz",
    "country": "Iran",
    "latitude": "31.35N",
    "longitude": "49.01E"
}
```

**Following question 1: assume the returned entry has been found erroneous. The actual average temperature of this entry is 2.5 degrees lower. Update this entry.**

**Request**

``` curl
curl --location --request PATCH 'http://127.0.0.1:8080/v1/temperatures?city=Ahvaz&dt=2013-07-01' \
--header 'Content-Type: application/json' \
--data-raw '{
    "averagetemperature": 36.65600000000001
}'
```

**Response**

``` json
{
    "dt": "2013-07-01",
    "averagetemperature": 36.65600000000001,
    "averagetemperatureuncertainty": 0.37,
    "city": "Ahvaz",
    "country": "Iran",
    "latitude": "31.35N",
    "longitude": "49.01E"
}
```