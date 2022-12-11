"""_summary_
@file       application_execution_model_v0_1.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models task execution actions.
@version    0.0.1
@date       2022-12-10
"""

import copy
import sys


class ApplicationExecutionModel_V0_1:
    """_summary_
    Tasks generate output values dependent on their input values.
    """

    def __init__(self):
        pass

    def process_step(self, outputs, inputs):
        # Get the current step
        step = [
            list(outputs["steps"].keys())[-1],
            outputs["steps"][list(outputs["steps"].keys())[-1]],
        ]

        # For started tasks, eat dependencies.
        for device_name, device in step[1]["started_tasks"].items():
            for cpu_name, (task_name, task_duration) in device.items():
                # Remove dependencies from device cache (so they cannot be reused).
                dependencies = inputs[device_name]["tasks"][task_name]["execution"][
                    "dependencies"
                ]

                for dependency in dependencies:
                    del inputs[device_name]["cache"][dependency]

                # Add dependencies to the tasks in the outputs.
                device[cpu_name].append({"dependencies": dependencies})

        # Move started tasks into running tasks and deduct N cycles to prepare
        # for next timestep.
        step[1]["running_tasks"] = copy.deepcopy(step[1]["started_tasks"])

        timestep = (
            outputs["next_timestep"]
            - outputs["steps"][list(outputs["steps"].keys())[-1]]["timestep"]
        )

        for device_name, device in step[1]["running_tasks"].items():
            for cpu_name, (task_name, task_duration, dependencies) in device.items():
                remaining_duration = task_duration - timestep
                if remaining_duration == 0:
                    if device_name not in step[1]["ending_tasks"]:
                        step[1]["ending_tasks"][device_name] = {}
                    step[1]["ending_tasks"][device_name][cpu_name] = (
                        task_name,
                        task_duration - timestep,
                        dependencies
                    )
                    # NOTE: cannot del from running_tasks here in loop.
                else:
                    step[1]["running_tasks"][device_name][cpu_name] = (
                        task_name,
                        task_duration - timestep,
                        dependencies
                    )

        # For tasks with no time left, generate outputs and remove from list.
        for device_name, device in step[1]["ending_tasks"].items():
            for cpu_name, (task_name, task_duration, data) in device.items():
                del step[1]["running_tasks"][device_name][cpu_name]

                task_outputs = inputs[device_name]["tasks"][task_name]["execution"][
                    "outputs"
                ]

                # NOTE: Add outputs to the cache of associated devices. In this
                # implementation, the output values are generated from a user
                # provided function that may or may not take in input values.

                # Get user provided function.
                fp_str, func_str = inputs[device_name]["tasks"][task_name]["execution"]["execution_func"]
                mod = __import__(f"{fp_str}")
                func = getattr(mod, func_str)
                data["results"] = func(len(data["dependencies"]), data["dependencies"])
                del data["dependencies"]

                for (output_id, output_targets), result in zip(task_outputs.items(), data["results"]):
                    for output_target in output_targets:
                        inputs[output_target]["cache"][output_id] = result

    def get_model_name(self):
        return "ApplicationExecutionModel_V0_1"
