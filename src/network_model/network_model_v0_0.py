"""_summary_
@file       network_model_v0_0.py
@author     Allen Jiang (alljiang@hotmail.com), Matthew Yu (matthewjkyu@gmail.com)
@brief      Models device network communication.
@version    0.0.0
@date       2022-11-28
"""

import copy
import sys

from network_model_interface import NetworkModelInterface


class NetworkModel_V0_0(NetworkModelInterface):
    """_summary_
    ApplicationModel_V0_0 models a very abstract interpretation of NoS
    interdevice communication. It has the following characteristics:
    - devices have a list of logical devices that they can communicate with.
    - transmission of data between devices is instantaneous.
    - data is represented as a single communication event.

    NOTE: V0.1 (Network expansion 1) has the following characteristics:
    - devices have a physical location in space.
    - devices have a communication range that determines who they can talk to.
    """

    def __init__(self) -> None:
        super().__init__()

    def add_device(self, device_name, device) -> bool:
        """_summary_
        Adds a device to the network model. A device must have the following
        attributes:
        - a device name (str)
        - a list of communicable devices (list(str))

        Args:
            device_name (_type_): _description_
            device (_type_): _description_

        Returns:
            bool: _description_
        """

        return super().add_device(device_name, device)

    def generate_network_graph(self, event_timeline) -> dict:
        # Plot event network communication on the graph.

        # for each event in the timeline
        for event in event_timeline:
            # get the actors in the event
            pass

        return super().generate_network_graph()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    try:
        import pretty_traceback

        pretty_traceback.install()
    except ImportError:
        pass  # no need to fail because of missing dev dependency

    model = NetworkModel_V0_0()

    device_0 = {"device_name": "device_0", "neighbors": ["device_1"]}

    device_1 = {"device_name": "device_1", "neighbors": ["device_0"]}

    model.add_device(device_0["device_name"], device_0)
    model.add_device(device_1["device_name"], device_1)

    event_timeline = [
        {
            "timestamp": 0,
            "devices": {
                "device_0": {"cores": {"core_0": "task_A"}, "hw": ["adc_0"]},
                "device_1": {"cores": {"core_0": "task_AA"}, "hw": []},
            },
            "cache": [{"output_0": ["device_0"]}, {}],
        },
        {
            "timestamp": 1,
            "devices": {
                "device_0": {"cores": {"core_0": "task_B"}, "hw": ["comm_0"]},
                "device_1": {"cores": {"core_0": "task_AA"}, "hw": []},
            },
            "cache": [{"output_1": ["device_1"]}, {}],
        },
        {
            "timestamp": 2,
            "devices": {
                "device_0": {"cores": {}, "hw": []},
                "device_1": {"cores": {"core_0": "task_C"}, "hw": ["comm_0"]},
            },
            "cache": [{"output_2": ["device_1"]}],
        },
        {
            "timestamp": 3,
            "devices": {
                "device_0": {"cores": {}, "hw": []},
                "device_1": {
                    "cores": {"core_0": "task_D", "core_1": "task_F"},
                    "hw": [],
                },
            },
            "cache": [{}, {"output_3": ["device_1"]}],
        },
        {
            "timestamp": 4,
            "devices": {
                "device_0": {"cores": {}, "hw": []},
                "device_1": {"cores": {"core_1": "task_G"}, "hw": []},
            },
            "cache": [{"output_4": ["device_1"]}],
        },
        {
            "timestamp": 5,
            "devices": {
                "device_0": {"cores": {}, "hw": []},
                "device_1": {"cores": {"core_1": "task_H"}, "hw": []},
            },
            "cache": [{"output_5": ["device_1"]}],
        },
        {
            "timestamp": 6,
            "devices": {
                "device_0": {"cores": {}, "hw": []},
                "device_1": {"cores": {"core_0": "task_E"}, "hw": []},
            },
            "cache": [{"output_7": ["device_1"]}],
        },
    ]

    network_graph = model.generate_network_graph(event_timeline)
    print(network_graph)
    model.print_network_graph()
    model.visualize_network_graph()
