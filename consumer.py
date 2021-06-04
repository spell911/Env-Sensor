from kafka import KafkaConsumer
from json import loads
from time import sleep
from db.insert_data import insert_data
from _cons import KAFKA_GROUP, KAFKA_BOOTSTRAP_SERVER, TABLE

import multiprocessing as mp


def insert_consume(kafka_topic):
    """
    Consume device data by topic, and insert theme to each device table

    Args:
        consumer (object): consumer by each topic devices
        table (str): name of device table 

    """
    consumer = KafkaConsumer(kafka_topic,
                             group_id=KAFKA_GROUP,
                             bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
                             value_deserializer=lambda x: loads(x.decode('utf-8')))

    for data in consumer:
        print("%s:%d:%d: key=%s value=%s" % (data.topic, data.partition,
                                             data.offset, data.key,
                                             data.value))
        insert_data(kafka_topic, data.value)

    pass


if __name__ == "__main__":
    # insert the consume data to postgres
    consume_00 = mp.Process(target=insert_consume,
                            args=('device_00',))
    consume_1c = mp.Process(target=insert_consume,
                            args=('device_1c',))
    consume_b8 = mp.Process(target=insert_consume,
                            args=('device_b8',))
    # start parallels consumers
    consume_00.start()
    consume_1c.start()
    consume_b8.start()
