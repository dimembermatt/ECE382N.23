"""_summary_
@file       energy_device.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Manages the energy consumption for a given device over time.
@version    0.0.0
@date       2022-10-21
"""

from energy_layer.energy_component import EnergyComponent;
from energy_layer.energy_powersupply import EnergyPowersupply;

class EnergyDevice:
    """_summary_
    Estimates and models the energy consumption of a given device. This
    consumption can be broken down into three components: processing, data
    acquisition, actuator control, and data transmission.
    """

    device_id = 0

    def __init__():
        """_summary_
        An application device has at least the following:
         - Hardware resources, including CPUs, ADCs, DACs, transceivers, etc
         - Software scheduler for determining how processes run on the hardware.
        """

        self.device_id = EnergyDevice.device_id
        EnergyDevice.device_id += 1

    def get_device_id(self):
        return self.device_id
