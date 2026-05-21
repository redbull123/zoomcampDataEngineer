#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--year', default=2021, type=int, help='Year of the taxi data')
@click.option('--month', default=1, type=int, help='Month of the taxi data')
@click.option('--username', default='root', type=str, help='Database username')
@click.option('--password', default='root', type=str, help='Database password')
@click.option('--port', default=5432, type=int, help='Database port')
@click.option('--database', default='ny_taxi', type=str, help='Database name')
@click.option('--chunk-size', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--table-name', default='yellow_taxi_data', type=str, help='Name of the table to store data')
@click.option('--hostname', default='localhost', type=str, help='Database hostname')

def run(year, month, username, password, port, database, chunk_size, table_name, hostname):
    df_iter = pd.read_csv(
    prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=chunk_size)


    engine = create_engine(f'postgresql+psycopg://{username}:{password}@{hostname}:{port}/{database}')


    first_chunk = next(df_iter)

    first_chunk.head(0).to_sql(
    name=f"{table_name}",
    con=engine,
    if_exists="replace"
    )

    print("Table created")

    first_chunk.to_sql(
    name=f"{table_name}",
    con=engine,
    if_exists="append"
    )

    print("Inserted first chunk:", len(first_chunk))

    for df_chunk in df_iter:
        df_chunk.to_sql(
        name=f"{table_name}",
        con=engine,
        if_exists="append"
    )
        print("Inserted chunk:", len(df_chunk))


if __name__ == "__main__":
    run()


