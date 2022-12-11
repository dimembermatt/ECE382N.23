"""_summary_
@file       application_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device applications.
@version    0.0.0
@date       2022-12-09
"""


import json
import sys

import matplotlib.pyplot as plt
from colorhash import ColorHash

from application_model.execution_model.application_execution_model_v0_0 import \
    ApplicationExecutionModel_V0_0
from application_model.execution_model.application_execution_model_v0_1 import \
    ApplicationExecutionModel_V0_1
from application_model.hardware_model.application_hardware_model_v0_0 import \
    ApplicationHardwareModel_V0_0
from application_model.timing_model.application_timing_model_v0_0 import \
    ApplicationTimingModel_V0_0
from application_model.timing_model.application_timing_model_v0_1 import \
    ApplicationTimingModel_V0_1


def get_app_hardware_models(hardware_model_str):
    match hardware_model_str:
        case "ApplicationHardwareModel_V0_0":
            return ApplicationHardwareModel_V0_0()
        case "ApplicationHardwareModel_V0_1":
            return None
        case _:
            return None


def get_app_execution_models(execution_model_str):
    match execution_model_str:
        case "ApplicationExecutionModel_V0_0":
            return ApplicationExecutionModel_V0_0()
        case "ApplicationExecutionModel_V0_1":
            return ApplicationExecutionModel_V0_1()
        case _:
            return None


def get_timing_models(timing_model_str):
    match timing_model_str:
        case "ApplicationTimingModel_V0_0":
            return ApplicationTimingModel_V0_0()
        case "ApplicationTimingModel_V0_1":
            return ApplicationTimingModel_V0_1()
        case "ApplicationTimingModel_V0_2":
            return None
        case "ApplicationTimingModel_V0_3":
            return None
        case _:
            return None


class ApplicationModelInterface:
    def __init__(
        self, path, inputs, hardware_model_str, execution_model_str, timing_model_str
    ):
        sys.path.append(path)
        self.timing_model = get_timing_models(timing_model_str)
        self.execution_model = get_app_execution_models(execution_model_str)
        self.hardware_model = get_app_hardware_models(hardware_model_str)
        self.inputs = inputs
        self.outputs = {"next_timestep": 0, "steps": {}}

        print("Running the following application submodel sub-submodels:")
        print(f"\t-Timing Model: {self.timing_model.get_model_name()}")
        print(f"\t-Execution Model: {self.execution_model.get_model_name()}")
        print(f"\t-Hardware Model: {self.hardware_model.get_model_name()}")

    def generate_output(self, num_steps=None):
        if num_steps is None:
            while True:
                can_run = self.timing_model.process_step(self.outputs, self.inputs)
                if can_run is False:
                    break
                self.execution_model.process_step(self.outputs, self.inputs)
                self.hardware_model.process_step(self.outputs, self.inputs)

        else:
            for _ in range(num_steps):
                can_run = self.timing_model.process_step(self.outputs, self.inputs)
                if can_run is False:
                    break
                self.execution_model.process_step(self.outputs, self.inputs)
                self.hardware_model.process_step(self.outputs, self.inputs)

    def print_outputs(self):
        print(json.dumps(self.outputs, indent=4))

    # def visualize_event_timeline(self):

    # def save_outputs(self):
