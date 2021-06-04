# dataset path
PATH_TO_DATA = "data_set/iot_telemetry_data.csv"
# kafka
KAFKA_GROUP = "env-device"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
# postgres
TABLE = 'iot_telemetry'
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost:5432/env_sensor"