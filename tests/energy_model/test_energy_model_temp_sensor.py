"""_summary_
@file       test_energy_model_temp_sensor.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for testing the energy model. The device under test
            is a TM4C masquerading as a temperature sensor.
@version    0.0.0
@data       2022-10-28
"""

import sys

sys.path.append("../../")

from src.energy_model.energy_model_interface import get_energy_model


def test_default_app():
    model = get_energy_model("EnergyModel_V0_0", "../../")
    device_0 = {
        "device_name": "TM4C",
        "cores": {
            "core_0": {
                "frequency": 1,
                "active_energy": 5,
                "idle_energy": 1,
            }
        },
        "peripherals": {
            "uart_0": {
                "active_energy": 3,
                "idle_energy": 1,
            },
            "adc_0": {
                "active_energy": 2,
                "idle_energy": 1
            }
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "Initialize ADC",
                    "duration": 30,
                    "dependencies": [],
                    "outputs": {
                        "adc_struct": ["TM4C"]
                    },
                    "hw": []
                },
                {
                    "task_name": "Sample ADC",
                    "duration": 15,
                    "dependencies": ["adc_struct"],
                    "outputs": {
                        "adc_measurement": ["TM4C"],
                    },
                    "hw": [
                        "adc_0",
                    ],
                },
                {
                    "task_name": "Filter ADC value",
                    "duration": 20,
                    "dependencies": ["adc_measurement"],
                    "outputs": {
                        "adc_output": [],
                    },
                    "hw": [
                        "uart_0"
                    ]
                }
            ]
        },
        "supply_id": "supply_0"
    }
    supply_0 = {
        "supply_name": "supply_0",
        "supply_voltage": 5.0,
        "max_supply_current": 5.0
    }
    model.add_device(device_0["device_name"], device_0)
    model.add_energy_supply(supply_0["supply_name"], supply_0)

    event_timeline = [{"timestamp": 0, "duration": 30.0, "devices": {"TM4C": {"cores": {"core_0": "Initialize ADC"}, "hw": []}}, "cache": [{"adc_struct": ["TM4C"]}]}, {"timestamp": 30.0, "duration": 15.0, "devices": {"TM4C": {"cores": {"core_0": "Sample ADC"}, "hw": ["adc_0"]}}, "cache": [{"adc_measurement": ["TM4C"]}]}, {"timestamp": 45.0, "duration": 20.0, "devices": {"TM4C": {"cores": {"core_0": "Filter ADC value"}, "hw": ["uart_0"]}}, "cache": [{"adc_output": []}]}]
    energy_usage = model.generate_energy_usage(event_timeline)
    print(energy_usage)
    model.print_energy_usage()
    model.save_outputs()
    model.visualize_energy_usage()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    test_default_app()
