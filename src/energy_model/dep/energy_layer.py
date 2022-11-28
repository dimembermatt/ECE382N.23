"""_summary_
@file       energy_layer.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Manages the devices energy consumption over time.
@version    0.0.0
@date       2022-10-20
"""

import sys

sys.path.append("../../src")


class EnergyLayer:
    """_summary_
    The energy layer consists of a set of mirroring devices to the application
    layer, each of which consists of energy models for the following:
    - processor: energy consumed for instructions/tasks executed
    - sensors/actuators: energy consumed for operating peripherals
    - transceivers: energy consumed for sending or receiving data
    """

    def __init__(self):
        pass

    # TODO: Methods that for each device during some timespan, given their
    # current operation, calculate the average energy usage.
