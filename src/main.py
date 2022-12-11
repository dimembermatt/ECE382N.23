"""_summary_
@file       main.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Simulates a given set of devices.
@version    0.0.0
@date       2022-12-11
"""

import json
import sys

from application_model.application_model_interface import \
    ApplicationModelInterface
from power_model.power_model_interface import PowerModelInterface


def load_inputs(path, specification_file):
    with open(f"{path}{specification_file}") as json_file:
        return json.load(json_file)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    try:
        import pretty_traceback

        pretty_traceback.install()
    except ImportError:
        pass  # no need to fail because of missing dev dependency

    path = "../tests/hello_world_device/"
    device_specification_file = "example_device.json"
    supply_specification_file = "example_power_supply.json"

    # Pass in our inputs
    device_inputs = load_inputs(path, device_specification_file)
    supply_inputs = load_inputs(path, supply_specification_file)

    # Select the model components
    app_model = ApplicationModelInterface(
        path,
        device_inputs,
        "ApplicationHardwareModel_V0_0",
        "ApplicationExecutionModel_V0_1",
        "ApplicationTimingModel_V0_3",
    )
    app_outputs = app_model.generate_output()

    power_model = PowerModelInterface(
        path,
        device_inputs,
        supply_inputs,
        app_outputs,
        "PowerConsumptionModel_V0_1",
        "PowerSupplyModel_V0_0",
    )
    power_outputs = power_model.generate_output()

    network_model = None

    app_model.pprint_outputs()
    power_model.pprint_outputs()

    # Call before visualize because matplotlib plot clears the figure.
    app_model.save_outputs()
    power_model.save_outputs()

    app_model.visualize_event_timeline()
    power_model.visualize_power_usage()
