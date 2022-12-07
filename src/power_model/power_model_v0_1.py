"""_summary_
@file       power_model_v0_1.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models device power usage.
@version    0.0.0
@date       2022-11-28
"""

import copy
import sys

from power_model_interface import PowerModelInterface


class PowerModel_V0_1(PowerModelInterface):
    """_summary_
    PowerModel_V0_1 (Power expansion 1) models a very abstract interpretation
    of the NoS power usage. It has the following characteristics:
    - multiple devices can share a single power source.
    - power consumption of CPU is based on the CPU utilization rate and
      characteristics (frequency, supply voltage, current draw).
    - the power source has voltage and current characteristics within some
      distribution.
    """

    def __init__(self) -> None:
        super().__init__("V0_1 Power Model")

    def add_device(self, device_name, device) -> bool:
        """_summary_
        Adds a device to the power model. A device must have the following
        attributes:
        - device name (str)
        - a set of cores and hardware peripherals, each with:
            - a static idle and active power consumption value (float, float)

        Args:
            device_name (_type_): _description_
            device (_type_): _description_

        Returns:
            bool: _description_
        """

        return super().add_device(device_name, device)

    def add_power_supply(self, supply_name, supply) -> bool:
        """_summary_
        Adds a power supply to the power model. A power supply must have the
        following attributes:
        - supply name (str)
        - a supply power characteristics, including supply voltage and maximum
          draw (float).

        Args:
            supply_name (_type_): _description_
            supply (_type_): _description_

        Returns:
            bool: _description_
        """
        return super().add_power_supply(supply_name, supply)

    def generate_power_usage(self, event_timeline):
        # Plot event power usage on the timeline.
        for device_id in self._devices.keys():
            self._devices[device_id]["events"] = []
            if self._devices[device_id]["supply_id"] in self._power_supplies:
                self._devices[device_id]["supply"] = self._power_supplies[
                    self._devices[device_id]["supply_id"]
                ]
                del self._devices[device_id]["supply_id"]

        for event in event_timeline:
            power_event = {
                "timestamp": event["timestamp"],
                "duration": event["duration"],
                "devices": {},
            }
            for device_id, device in event["devices"].items():
                device_info = self._devices[device_id]
                idle_consumers = [core for core in device_info["cores"]] + [
                    peripheral for peripheral in device_info["peripherals"]
                ]
                active_consumers = []

                for core_id in device["cores"].keys():
                    idle_consumers.remove(core_id)
                    active_consumers.append(core_id)

                for hw_id in device["hw"]:
                    idle_consumers.remove(hw_id)
                    active_consumers.append(hw_id)

                power_event["devices"][device_id] = []

                y = 0
                # Calculate power per consumer
                for consumer in active_consumers:
                    if "core" in consumer:
                        power_usage = device_info["cores"][consumer]["active_power"]
                    else:
                        power_usage = device_info["peripherals"][consumer][
                            "active_power"
                        ]

                    power_event["devices"][device_id].append(
                        [consumer, "active", power_usage]
                    )

                # Calculate power per consumer
                for consumer in idle_consumers:
                    if "core" in consumer:
                        power_usage = device_info["cores"][consumer]["idle_power"]
                    else:
                        power_usage = device_info["peripherals"][consumer]["idle_power"]

                    power_event["devices"][device_id].append(
                        [consumer, "idle", power_usage]
                    )

            self._power_usage.append(power_event)

        return super().generate_power_usage()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    try:
        import pretty_traceback

        pretty_traceback.install()
    except ImportError:
        pass  # no need to fail because of missing dev dependency

    model = PowerModel_V0_1()

    device_0 = {
        "device_name": "device_0",
        "cores": {
            "core_0": {
                "active_power": 5,  # Joules
                "idle_power": 1,  # Joules
            }
        },
        "peripherals": {
            "comm_0": {
                "active_power": 3,  # Joules
                "idle_power": 1,  # Joules
            },
            "adc_0": {
                "active_power": 2,  # Joules
                "idle_power": 1,  # Joules
            },
        },
        "supply_id": "supply_0",
    }

    device_1 = {
        "device_name": "device_1",
        "cores": {
            "core_0": {
                "active_power": 5,
                "idle_power": 1,
            },
            "core_1": {
                "active_power": 5,
                "idle_power": 1,
            },
        },
        "peripherals": {
            "comm_0": {
                "active_power": 3,  # Joules
                "idle_power": 1,  # Joules
            },
        },
        "supply_id": "supply_1",
    }

    model.add_device(device_0["device_name"], device_0)
    model.add_device(device_1["device_name"], device_1)

    supply_0 = {
        "supply_name": "supply_0",
        "supply_voltage": 5.0,  # 5V
        "max_supply_current": 5.0,  # 5A
    }

    supply_1 = {
        "supply_name": "supply_1",
        "supply_voltage": 5.0,  # 5V
        "max_supply_current": 2.5,  # 2.5A
    }

    model.add_power_supply(supply_0["supply_name"], supply_0)
    model.add_power_supply(supply_1["supply_name"], supply_1)

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

    power_usage = model.generate_power_usage(event_timeline)
    print(power_usage)
    model.print_power_usage()
    model.visualize_power_usage()
