"""_summary_
@file       test_app_model_temp_sensor.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for testing the application model. The device under test
            is a TM4C masquerading as a temperature sensor.
@version    0.0.0
@data       2022-10-28
"""

import sys

sys.path.append("../../")

from src.application_model.application_model_interface import \
    get_application_model


def test_default_app():
    model = get_application_model("ApplicationModel_V0_0", "../../")
    device_0 = {
        "device_name": "TM4C",
        "cores": {"core_0": {"frequency": 1}},
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
        }
    }

    model.add_device(device_0["device_name"], device_0)
    event_timeline = model.generate_event_timeline()
    print(event_timeline)
    model.print_event_timeline()
    model.save_outputs()
    model.visualize_event_timeline()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    test_default_app()
