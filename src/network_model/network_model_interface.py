"""_summary_
@file       network_model_interface.py
@author     Allen Jiang (alljiang@hotmail.com), Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device network
            communication.
@version    0.0.0
@date       2022-11-28
"""

import sys

import matplotlib.pyplot as plt
from colorhash import ColorHash


class NetworkModelInterface:
    def __init__(self) -> None:
        self._devices = {}
        self._network_graph = []
        self._fig, self._ax = None, None

    def add_device(self, device_name, device) -> bool:
        if device_name in self._devices:
            return False
        self._devices[device_name] = device
        return True

    def generate_network_graph(self) -> dict:
        pass

    def get_network_graph_step(self, step) -> (bool, dict):
        if step < 0 or step >= len(self._network_graph):
            return (False, {})
        else:
            return (True, self._network_graph[step])

    def print_network_graph(self) -> None:
        pass

    def visualize_network_graph(self) -> None:
        plt.tight_layout()
        plt.show()
