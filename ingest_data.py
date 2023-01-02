#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd


from sqlalchemy import create_engine

import pyarrow as pa

import pyarrow.parquet as pq

def main(params):
      user = params.user
      password = params.password
      host = params.host
      port = params.port
      db = params.db
      table_name = params.table.name
      url = params.url
      csv_name = 'output.csv'

      os.system(f"wget {url} -O {csv_name}")

      
      engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{db}')




      df_iter = pq.iter_batches().read_table('yellow_tripdata_2022-01.parquet')
      
      df_iter = df_iter.to_pandas()

      df = next(df_iter)

      df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
      df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

      df.head(n=0).to_sql(name=table, con=engine, if_exits='replace')

      df.to_sql(name='yellow_tripdata_trip', con=engine, if_exits = 'append')

      while True:
            try:
                  t_start = time()

                  df = next(df_iter)

                  df.tpep_pickup_datetime = pd.tp_datetime(df.tpep_pickup_datetime)
                  df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

                  df.to_sql(name=table_name,con=engine, if_exits='append')

                  t_end = time()

                  print('inserted another chunk, took %.3f second' %(t_end - t_start))

            except StopIteration:
                  print("Finished ingesting data into the postgres database")
                  break

if __name__ == '__main__':
      parser = argparse.ArgumentParser(description='Ingest Pargquet data to Postgres')

      parser.add_argument('--user',required=True, help='user name for postgres')
      parser.add_argument('--password', required=True, help='password for postgres')
      parser.add_argument('--host', required=True, help='host for postgres')
      parser.add_argument('--port', required=True, help='port for postgres')
      parser.add_argument('--db', required=True, help='database name for postgres')
      parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
      parser.add_argument('--url', required=True, help='url of the pargquet file')

      args = parser.parse_args()

      main(args)