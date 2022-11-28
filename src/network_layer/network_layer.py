
from time import time


class NetworkTransmission:
    def __init__(self, time_until_transmission, src_device, dst_device, message):
        self.time_until_transmission = time_until_transmission
        self.src_device = src_device
        self.dst_device = dst_device
        self.message = message

class NetworkLayer:
    """
     This class manages all devices, and queues/schedules/executes
     each message being sent between devices.
    """

    def __init__(self):
        self.device_dict = dict()
        self.transmission_queue = []

    def add_device(self, device_id, location=(0, 0, 0), transmission_range=0):
        if device_id in self.device_dict:
            raise Exception("Device " + str(device_id) + " already exists.")

        self.device_dict[device_id] = NetworkDevice(device_id, location, transmission_range)

    def get_device_list(self):
        device_list = list(self.device_dict.keys())
        device_list.sort()
        return device_list

    def __get_device(self, device_id):
        # make sure the device exists
        if device_id not in self.device_dict:
            raise Exception("Device " + str(device_id) + " does not exist.")

        return self.device_dict[device_id]

    def schedule_transmission(self, src_device_id, dst_device_id, message, time_until_transmission=0):
        src_device = self.__get_device(src_device_id)
        dst_device = self.__get_device(dst_device_id)

        transmission = NetworkTransmission(time_until_transmission, src_device, dst_device, message)
        self.transmission_queue.append(transmission)

    def step_layer(self):
        for transmission in self.transmission_queue:
            if transmission.time_until_transmission == 0:
                transmission.src_device.send_message(transmission.dst_device, transmission.message)
            else:
                transmission.time_until_transmission -= 1


class NetworkDevice:
    """
    This class exposes the transceivers on each device, 
    and their physical properties (transmission power, geometry, etc).
    """
    
    def __init__(self, device_id, device_location, transmission_range):
        self.transceiver = NetworkTransceiver(self, self.__receive_handler)
        self.device_id = device_id
        self.device_location = device_location
        self.transmission_range = transmission_range

    def __receive_handler(self, src_device, message):
        print(str(src_device) + " :: " + str(message))

    def get_device_id(self):
        return self.device_id

    def send_message(self, dst_device, message):
        dst_transceiver = dst_device.transceiver
        self.transceiver.send(dst_transceiver, message)

    def get_transceiver(self):
        return self.transceiver

    def __str__(self):
        return "NetworkDevice: " + str(self.device_id)
    

class NetworkTransceiver:
    """
    This class exposes the messages that are sent 
    or received between processes on the device.
    """

    def __init__(self, host_device, receive_handler):
        self.host_device = host_device
        self.transceiver_list = []
        self.receive_handler = receive_handler
    
    def __calculate_distance(self, other_device):
        x1, y1, z1 = self.host_device.device_location
        x2, y2, z2 = other_device.device_location

        return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5

    def receive_handler(self, source_device, message):
        """
        This method handles the received message from another transceiver
        """
        distance = self.__calculate_distance(source_device)

        # only receive if the message is within range
        if distance <= self.host_device.transmission_range:
            self.receive_handler(source_device, message)

    def send(self, dst_transceiver, message):
        """
        This method sends a message to another transceiver
        """
        dst_transceiver.receive_handler(self.host_device, message)


class NetworkMessage:
    """
    This class consists of messages generated by the application layer. 

    These messages are given attributes like packet length, communication 
    type, and other attributes of the communication stack necessary for transmission.
    """

    def __init__(self, message_type, message_length, message_payload):
        # TODO make sure these constraints are correct, depends on what is the data
        if type(message_payload) is not bytearray:
            raise TypeError("message_payload must be a bytearray")

        if type(message_length) is not int or message_length < 0:
            raise TypeError("message_length must be a positive integer")

        if type(message_type) is not str:
            raise TypeError("message_type must be a string")

        if message_length > len(message_payload):
            raise ValueError("message_length cannot be larger than the payload")

        self.message_type = message_type
        self.message_length = message_length
        self.message_payload = message_payload[0:message_length]
    
    def __str__(self):
        rv = ""

        rv += "Message Type: " + self.message_type + "\n"
        rv += "Message Length: " + str(self.message_length) + "\n"
        rv += "Message Payload: " + str(self.message_payload) + "\n"

        return rv
