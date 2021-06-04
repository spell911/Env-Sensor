# postgres
TABLE = 'iot_telemetry'
POSTGRES_ENDPOINT = 'postgres:123456@172.19.0.6:5432/env_sensor'
# airflow opt dags path
AIRFLOW_DAGS_PATH = '/opt/airflow/dags'
# sql
SQL_DEVICE_TS = """
    SELECT dev.device, MAX(dev.ts) AS curr_ts, COALESCE(MAX(iot.ts), 0) AS last_ts FROM device_{} AS dev
    LEFT JOIN iot_telemetry AS iot
    ON dev.device = iot.device
    WHERE dev.ts > COALESCE((select max(ts) from iot_telemetry as iot_2 where iot_2.device = '{}'), 0)
    GROUP BY dev.device;"""
SQL_DEVICE = """
    SELECT ts, device, co, humidity, light, lpg, motion, smoke, temp
    FROM {table} WHERE ts BETWEEN {last_ts} AND {curr_ts};"""
SQL_INSERT_IOT_TELEMERTY = """
    INSERT INTO iot_telemetry({columns})\nVALUES {values};"""
SENSOR_DEVICES = ['00:0f:00:70:91:0a',
                  '1c:bf:ce:15:ec:4d', 'b8:27:eb:bf:9d:51']
