"""_summary_
@file       application_execution_model.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      XXX
@version    0.0.0
@date       2022-12-09
"""


class ApplicationExecutionModel_V0_0:
    """_summary_
    Tasks consume dependencies and generate outputs without considering their
    actual values.
    """

    def __init__(self):
        pass

    def process_step(self, outputs, inputs):
        # Get the current step
        step = [
            list(outputs["steps"].keys())[-1],
            outputs["steps"][list(outputs["steps"].keys())[-1]],
        ]

        # For each task in each device and cpu, consume the relevant
        # dependencies and generate the relevant outputs.
        for device_name, device in step[1]["started_tasks"].items():
            for task_name, _ in device.values():
                # Remove dependencies from device cache (so they cannot be reused).
                dependencies = inputs[device_name]["tasks"][task_name]["execution"][
                    "dependencies"
                ]

                for dependency in dependencies:
                    del inputs[device_name]["cache"][dependency]

        for device_name, device in step[1]["ending_tasks"].items():
            for task_name, _ in device.values():
                task_outputs = inputs[device_name]["tasks"][task_name]["execution"][
                    "outputs"
                ]

                # NOTE: Add outputs to the cache of associated devices. In this
                # implementation, the input and output values don't matter.
                for output_id, output_targets in task_outputs.items():
                    for output_target in output_targets:
                        inputs[output_target]["cache"][output_id] = 1

    def get_model_name():
        return "ApplicationExecutionModel_V0_0"
