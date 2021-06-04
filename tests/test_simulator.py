from sensor_simulator import get_data_with_simulated
from _setup import ex_vars


def test_get_data_with_simulated():
    # test all devices we have at head
    for device in ex_vars:
        for data in get_data_with_simulated(device.head()):
            assert isinstance(data, dict) == True
