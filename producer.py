from json import dumps
from kafka import KafkaProducer
from _cons import KAFKA_BOOTSTRAP_SERVER
from _setup import ex_vars
from sensor_simulator import get_data_with_simulated

import multiprocessing as mp
import pandas as pd

device_00, device_1c, device_b8 = ex_vars


def get_partitioner(key, all, available):
    """
    Set kafka producer partitioner antribute

    Return:
        int, key number of specific partition we want to produce to
    """
    return 0


def producer_generator(device_data, kafka_topic):
    """
    Generate devices data to producers

    """
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER, value_serializer=lambda x:
                             dumps(x).encode('utf-8'), partitioner=get_partitioner)

    for data in get_data_with_simulated(device_data):

        producer.send(kafka_topic, data)
        print(f'Sending data: {data}')
    pass


if __name__ == "__main__":
    # produce to kafka broker
    produce_00 = mp.Process(target=producer_generator,
                            args=(device_00, 'device_00',))
    produce_1c = mp.Process(target=producer_generator,
                            args=(device_1c, 'device_1c',))
    produce_b8 = mp.Process(target=producer_generator,
                            args=(device_b8, 'device_b8',))
    # start parallels producers
    produce_00.start()
    produce_1c.start()
    produce_b8.start()
