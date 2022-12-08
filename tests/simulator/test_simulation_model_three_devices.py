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

from src.application_model.application_model_interface import get_application_model
from src.energy_model.energy_model_interface import get_energy_model
from src.network_model.network_model_v0_0 import NetworkModel_V0_0


def test_default_app():
    app_model = get_application_model("ApplicationModel_V0_1", CWD)
    energy_model = get_energy_model("EnergyModel_V0_1", CWD)
    network_model = NetworkModel_V0_0()

    device_0 = {
        "device_name": "Alexa",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 20,
                "idle_energy": 3,
            }
        },
        "peripherals": {
            "modem": {
                "active_energy": 0,
                "idle_energy": 0,
            },
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "Read Sensors",
                    "duration": 3,
                    "dependencies": ["temperature", "motion"],
                    "outputs": {"ac_on": ["AC"]},
                    "hw": [],
                },
                {
                    "task_name": "Turn On AC",
                    "duration": 20,
                    "dependencies": [],
                    "outputs": {"ac_off": ["AC"]},
                    "hw": ["modem"],
                },
                {
                    "task_name": "Turn Off AC",
                    "duration": 10,
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
            ]
        },
        "supply_id": "supply_0",
    }

    device_1 = {
        "device_name": "TS1",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 20,
                "idle_energy": 3,
            }
        },
        "peripherals": {
            "adc": {
                "active_energy": 5,
                "idle_energy": 3,
            }
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "Sense Temperature",
                    "duration": 1,
                    "dependencies": [],
                    "outputs": {
                        "temperature": ["Alexa"],
                    },
                    "hw": [
                        "adc",
                    ],
                },
                {
                    "task_name": "Idle",
                    "duration": 5,
                    "dependencies": [""],
                    "outputs": {},
                    "hw": [""],
                },
            ]
        },
        "supply_id": "supply_0",
    }

    device_5 = {
        "device_name": "AC",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 20,
                "idle_energy": 3,
            }
        },
        "peripherals": {
            "hvac": {
                "active_energy": 30,
                "idle_energy": 0,
            }
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "Idle",
                    "duration": 4,
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
                {
                    "task_name": "AC_Running",
                    "duration": 20,
                    "dependencies": ["ac_on"],
                    "outputs": {},
                    "hw": ["hvac"],
                },
                {
                    "task_name": "Stopped",
                    "duration": 10,
                    "dependencies": ["ac_off"],
                    "outputs": {},
                    "hw": [],
                },
            ]
        },
        "supply_id": "supply_0",
    }

    device_6 = {
        "device_name": "MS",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 20,
                "idle_energy": 3,
            }
        },
        "peripherals": {
            "adc": {
                "active_energy": 8,
                "idle_energy": 3,
            }
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "Motion Sensing",
                    "duration": 1,
                    "dependencies": [],
                    "outputs": {
                        "motion": ["Alexa"],
                    },
                    "hw": ["adc"],
                },
                {
                    "task_name": "Idle",
                    "duration": 5,
                    "dependencies": [""],
                    "outputs": {},
                    "hw": [""],
                },
            ]
        },
        "supply_id": "supply_0",
    }

    supply_0 = {
        "supply_name": "supply_0",
        "supply_voltage": 5.0,
        "max_supply_current": 5.0,
    }

    devices = [device_0, device_1, device_5, device_6]
    for device in devices:
        app_model.add_device(device["device_name"], device)
        energy_model.add_device(device["device_name"], device)
        network_model.add_device(device["device_name"], device)
    energy_model.add_energy_supply(supply_0["supply_name"], supply_0)

    event_timeline = app_model.generate_event_timeline()
    energy_usage = energy_model.generate_energy_usage(event_timeline)

    app_model.save_outputs()
    app_model.visualize_event_timeline()

    energy_model.save_outputs()
    energy_model.visualize_energy_usage()

    network_graph = network_model.generate_network_graph(event_timeline)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    test_default_app()
