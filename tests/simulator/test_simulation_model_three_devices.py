"""_summary_
@file       test_simulation_model_three_devices.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for modeling. Tests three devices communicating to each
            other in a round robin fashion.
@version    0.0.0
@data       2022-10-28
"""

import sys

CWD = "../../"
sys.path.append(CWD)

from src.application_model.application_model_interface import \
    get_application_model
from src.energy_model.energy_model_interface import get_energy_model


def test_default_app():
    app_model = get_application_model("ApplicationModel_V0_1", CWD)
    energy_model = get_energy_model("EnergyModel_V0_0", CWD)

    device_0 = {
        "device_name": "dev0",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 5,
                "idle_energy": 1,
            }
        },
        "peripherals": {
            "comm_0": {
                "active_energy": 20,
                "idle_energy": 2,
            },
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "send_message_to_dev1",
                    "duration": 20,
                    "dependencies": [],
                    "outputs": {
                        "message_0": ["dev1"]
                    },
                    "hw": ["comm_0"]
                },
                {
                    "task_name": "send_message_to_dev1",
                    "duration": 10,
                    "dependencies": ["message_2"],
                    "outputs": {
                        "message_3": ["dev1"]
                    },
                    "hw": ["comm_0"]
                },
                {
                    "task_name": "send_message_to_dev1",
                    "duration": 2,
                    "dependencies": ["message_5"],
                    "outputs": {
                        "message_6": ["dev1"]
                    },
                    "hw": ["comm_0"]
                },
            ]
        },
        "supply_id": "supply_0"
    }
    device_1 = {
        "device_name": "dev1",
        "cores": {
            "core_0": {
                "frequency": 2,
                "active_energy": 5,
                "idle_energy": 1,
            }
        },
        "peripherals": {
            "comm_0": {
                "active_energy": 25,
                "idle_energy": 5,
            },
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "send_message_to_dev2",
                    "duration": 8,
                    "dependencies": ["message_0"],
                    "outputs": {
                        "message_1": ["dev2"]
                    },
                    "hw": ["comm_0"]
                },
                {
                    "task_name": "send_message_to_dev2",
                    "duration": 5,
                    "dependencies": ["message_3"],
                    "outputs": {
                        "message_4": ["dev2"]
                    },
                    "hw": ["comm_0"]
                },
                {
                    "task_name": "send_message_to_dev2",
                    "duration": 3,
                    "dependencies": ["message_6"],
                    "outputs": {
                        "message_7": ["dev2"]
                    },
                    "hw": ["comm_0"]
                },
            ]
        },
        "supply_id": "supply_0"
    }
    device_2 = {
        "device_name": "dev2",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 5,
                "idle_energy": 1,
            }
        },
        "peripherals": {
            "comm_0": {
                "active_energy": 10,
                "idle_energy": 1,
            },
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "send_message_to_dev0",
                    "duration": 10,
                    "dependencies": ["message_1"],
                    "outputs": {
                        "message_2": ["dev0"]
                    },
                    "hw": ["comm_0"]
                },
                {
                    "task_name": "send_message_to_dev0",
                    "duration": 5,
                    "dependencies": ["message_4"],
                    "outputs": {
                        "message_5": ["dev0"]
                    },
                    "hw": ["comm_0"]
                },
                {
                    "task_name": "send_message_to_dev0",
                    "duration": 2,
                    "dependencies": ["message_7"],
                    "outputs": {
                        "message_8": ["dev0"]
                    },
                    "hw": ["comm_0"]
                },
            ]
        },
        "supply_id": "supply_0"
    }
    supply_0 = {
        "supply_name": "supply_0",
        "supply_voltage": 5.0,
        "max_supply_current": 5.0
    }

    devices = [device_0, device_1, device_2]
    for device in devices:
        app_model.add_device(device["device_name"], device)
        energy_model.add_device(device["device_name"], device)
    energy_model.add_energy_supply(supply_0["supply_name"], supply_0)

    event_timeline = app_model.generate_event_timeline()
    energy_usage = energy_model.generate_energy_usage(event_timeline)

    app_model.save_outputs()
    app_model.visualize_event_timeline()

    energy_model.save_outputs()
    energy_model.visualize_energy_usage()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    test_default_app()
