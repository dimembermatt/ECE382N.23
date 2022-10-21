
import sys

sys.path.append("../src")

from network_layer.network_layer import *

if __name__ == "__main__":
    if int(sys.version[0]) < 3:
        raise Exception("This program only supports Python 3.")

    layer = NetworkLayer()

    layer.add_device(0)
    layer.add_device(1)

    device_list = layer.get_device_list()
    assert len(device_list) == 2

    id_0 = device_list[0]
    id_1 = device_list[1]

    # length = 4, so 4 and 5 are ignored
    message = NetworkMessage("test", 4, bytearray([0, 1, 2, 3, 4, 5]))
    layer.schedule_transmission(id_0, id_1, message)
    
    layer.step_layer()

    