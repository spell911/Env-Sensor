from time import time, sleep

import json
import pandas as pd


def get_data_with_simulated(device_data):
    """
    Simulation the data streamline and send to kafka producer

    Args:
        device_data (dataframe): dataframe of each device.

    Yield:
        (dict), generate data
    """
    for idx, row in device_data.iterrows():
        # Convert row data to json format
        result = row.to_json(orient="index")
        parsed = json.loads(result)
        # Waiting...
        sleep(1)
        yield parsed
