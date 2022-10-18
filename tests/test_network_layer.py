
import sys

sys.path.append("../")

from network_layer.network_layer import NetworkMessage

if __name__ == "__main__":
    if int(sys.version[0]) < 3:
        raise Exception("This program only supports Python 3.")

    message = NetworkMessage("test", 4, bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

    print(message)

    