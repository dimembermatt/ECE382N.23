"""_summary_
@file       application_timing_model_v0_1.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models timing interactions between tasks.
@version    0.0.1
@date       2022-12-10
"""


class ApplicationTimingModel_V0_1:
    """_summary_
    Tasks in a schedule are ordered temporally and each task has a given task
    duration in cycles.
    """

    def __init__(self):
        pass

    def process_step(self, outputs, inputs):
        # time ---------------------------------------> time + N
        # start tasks -> running tasks -> end tasks
        # eat deps       deduct N cycles  generate outputs

        executable_tasks = []

        # Extract the imminent task from each device.
        for device_name, device in inputs.items():
            for cpu_name, cpu in device["schedule"].items():
                if len(cpu) > 0:
                    task_name = cpu.pop(0)

                    # Check if all dependencies are fulfilled.
                    dependencies = inputs[device_name]["tasks"][task_name]["execution"][
                        "dependencies"
                    ]
                    deps_fulfilled = True
                    for dependency in dependencies:
                        if dependency not in inputs[device_name]["cache"]:
                            deps_fulfilled = False

                    if deps_fulfilled:
                        executable_tasks.append(
                            [
                                device_name,
                                cpu_name,
                                task_name,
                                inputs[device_name]["tasks"][task_name]["timing"][
                                    "level_0"
                                ]["duration"],
                            ]
                        )
                    else:
                        cpu.insert(0, task_name)

        # NOTE: Since we assume here that each task executing has a task
        # duration, choose the next timestep based on the closest duration to 0.
        step = {
            "timestep": outputs["next_timestep"],
            "started_tasks": {},
            "running_tasks": {},
            "ending_tasks": {},
        }

        min_duration = None
        if len(outputs["steps"]) > 0:
            # Copy over running tasks from previous step.
            step["running_tasks"] = outputs["steps"][list(outputs["steps"].keys())[-1]][
                "running_tasks"
            ]
            for device_name, device in step["running_tasks"].items():
                for cpu_name, (task_name, task_duration) in device.items():
                    if min_duration is None or min_duration > task_duration:
                        min_duration = task_duration

        for device_name, cpu_name, task_name, task_duration in executable_tasks:
            step["started_tasks"][device_name] = {cpu_name: [task_name, task_duration]}
            if min_duration is None or min_duration > task_duration:
                min_duration = task_duration

        outputs["steps"][outputs["next_timestep"]] = step

        if min_duration is None:
            # No tasks left to execute.
            outputs["next_timestep"] = "End of schedule."
            return False
        else:
            outputs["next_timestep"] = step["timestep"] + min_duration
            return True

    def get_model_name(self):
        return "ApplicationTimingModel_V0_1"
