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
    specification_file = "example_device.json"

    # Pass in our inputs
    inputs = load_inputs(path, specification_file)

    # Select the model components
    app_model = ApplicationModelInterface(
        path,
        inputs,
        "ApplicationHardwareModel_V0_0",
        "ApplicationExecutionModel_V0_1",
        "ApplicationTimingModel_V0_2",
    )
    power_model = None
    network_model = None

    app_model.generate_output()

    app_model.pprint_outputs()

    # Call before visualize because matplotlib plot clears the figure.
    app_model.save_outputs()

    app_model.visualize_event_timeline()
