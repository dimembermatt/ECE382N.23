"""_summary_
@file       application_execution_model_v0_0.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models task execution actions.
@version    0.0.0
@date       2022-12-10
"""

import copy


class ApplicationExecutionModel_V0_0:
    """_summary_
    Tasks consume dependencies and generate outputs without considering their
    actual values.
    """

    def __init__(self):
        pass

    def process_step(self, outputs, inputs):
        if outputs["next_timestep"] == "End of schedule.":
            return

        # Get the current step
        step = [
            list(outputs["steps"].keys())[-1],
            outputs["steps"][list(outputs["steps"].keys())[-1]],
        ]

        # For started tasks, eat dependencies.
        for device_name, device in step[1]["started_tasks"].items():
            for cpu_name, (task_name, task_duration) in device.items():
                # Remove dependencies from device cache (so they cannot be reused).
                dependency_keys = inputs[device_name]["tasks"][task_name]["execution"][
                    "dependencies"
                ]
                dependency_values = []
                for dependency_key in dependency_keys:
                    dependency_values.append(
                        inputs[device_name]["cache"][dependency_key]
                    )
                    del inputs[device_name]["cache"][dependency_key]

                # Add dependencies to the tasks in the outputs.
                device[cpu_name].append({"dependencies": dependency_values})

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
                        dependencies,
                    )
                    # NOTE: cannot del from running_tasks here in loop.
                else:
                    step[1]["running_tasks"][device_name][cpu_name] = (
                        task_name,
                        task_duration - timestep,
                        dependencies,
                    )

        # For tasks with no time left, generate outputs and remove from list.
        for device_name, device in step[1]["ending_tasks"].items():
            for cpu_name, (task_name, task_duration, data) in device.items():
                del step[1]["running_tasks"][device_name][cpu_name]
                if len(step[1]["running_tasks"][device_name]) == 0:
                    del step[1]["running_tasks"][device_name]

                task_outputs = inputs[device_name]["tasks"][task_name]["execution"][
                    "outputs"
                ]

                # NOTE: Add outputs to the cache of associated devices. In this
                # implementation, the input and output values don't matter.
                data["results"] = [1] * len(
                    inputs[device_name]["tasks"][task_name]["execution"][
                        "outputs"
                    ].keys()
                )
                del data["dependencies"]

                for (output_id, output_targets), result in zip(
                    task_outputs.items(), data["results"]
                ):
                    for output_target in output_targets:
                        inputs[output_target]["cache"][output_id] = result

    def get_model_name(self):
        return "ApplicationExecutionModel_V0_0"
