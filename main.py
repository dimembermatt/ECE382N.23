"""_summary_
@file       main.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for simulating IoT networks.
@version    0.0.0
@data       2022-10-08
"""

import sys

from src.application_layer.application_layer import ApplicationLayer

# from src.network_layer.network_layer import NetworkLayer
# from src.energy_layer.energy_layer import EnergyLayer


class Simulation:
    """_summary_
    Orchestrates communication between each layer and resolves graphical
    representations of each.
    """

    def __init__(self):
        app_layer = ApplicationLayer()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    sim = Simulation()
