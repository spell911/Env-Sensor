from sqlalchemy import create_engine
from time import sleep, localtime, strftime
from etl_process_cons import TABLE, POSTGRES_ENDPOINT, AIRFLOW_DAGS_PATH, SQL_DEVICE_TS, SQL_DEVICE, SQL_INSERT_IOT_TELEMERTY, SENSOR_DEVICES
from os import path

import os.path
import pandas as pd
import psycopg2
import json
import glob

# Create the database engine
engine = create_engine(
    'postgresql+psycopg2://{}'.format(POSTGRES_ENDPOINT))


def extract_from_db():
    """
    Read devices data from postgres db and save them to csv file in temp folder

    """
    # Get last timestamp of each device
    devices_ts = []
    for device in SENSOR_DEVICES:
        df = pd.read_sql(SQL_DEVICE_TS.format(device[:2], device), engine)

        devices_ts.append(df)
    devices_ts = pd.concat(devices_ts)
    # Get data to dataframe and save to csv
    for idx, row in devices_ts.iterrows():
        print('device, curr_ts, last_ts : {} {} {}'.format(
            row['device'], row['curr_ts'], row['last_ts']))

        pd.read_sql(SQL_DEVICE.format(table='device_{}'.format(row['device'][:2]), last_ts=row['last_ts'], curr_ts=row['curr_ts']), engine).to_csv(
            '{}/iot_temp_data/device_{}.csv'.format(AIRFLOW_DAGS_PATH, row['device'][:2]), index=False)

    pass


def transform_data():
    """
    Convert boolean columns to int then combine all devices data to temp folder

    """
    csv_files = glob.glob('{}/iot_temp_data/*.csv'.format(AIRFLOW_DAGS_PATH))
    df_all = []

    for f in csv_files:
        df = pd.read_csv(f)
        # convert boolean to nubmer for plot the graph
        df['light'] = convert_boolean_to_int(df['light'])
        df['motion'] = convert_boolean_to_int(df['motion'])
        # append all data for concat theme
        df_all.append(df)

    if len(df_all) > 0:
        df_all = pd.concat(df_all)
        # sort all devices by timestamp
        df_all.sort_values(by=['ts'], inplace=True)
        print(df_all.head())
        df_all.to_csv(
            '{}/iot_temp_data/iot_telemetry_temp.csv'.format(AIRFLOW_DAGS_PATH), index=False)

    pass


def convert_boolean_to_int(df_val):
    """
    Return boolean value to number: True is 1, False is 0

    """
    return df_val.astype('int32')


def load_to_db():
    """
    Insert combined data to postgres db

    """
    if path.exists('{}/iot_temp_data/iot_telemetry_temp.csv'.format(AIRFLOW_DAGS_PATH)):
        df = pd.read_csv('{}/iot_temp_data/iot_telemetry_temp.csv'.format(AIRFLOW_DAGS_PATH),
                         nrows=None,
                         error_bad_lines=False,
                         warn_bad_lines=True)

        if not df.empty:
            for idx, row in df.iterrows():
                result = row.to_json(orient="index")
                parsed = json.loads(result)
                # get columns name by keys
                columns = list(parsed.keys())
                # print("\nkeys:", columns)
                # get rows values by values
                rows = list(parsed.values())
                # print("\nvalues:", rows)
                sql_insert = SQL_INSERT_IOT_TELEMERTY
                # wait a sec
                sleep(1*10**-8)
                engine.execute(sql_insert.format(columns=', '.join(
                    columns), values=tuple(rows)))
    pass


if __name__ == '__main__':
    # Extract data from db
    extract_from_db()
    # Transform data to analytics
    transform_data()
    # Load data to postgres table
    load_to_db()
