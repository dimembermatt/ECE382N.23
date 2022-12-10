"""_summary_
@file       application_timing_model_v0_0.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      XXX
@version    0.0.0
@date       2022-12-09
"""


class ApplicationTimingModel_V0_0:
    """_summary_
    Tasks in a schedule are ordered logically and each task is considered 1
    cyle regardless of true duration.
    """

    def __init__(self):
        pass

    def process_step(self, outputs, inputs):
        executable_tasks = []

        tasks_to_execute = False

        # Extract the imminent task from each device.
        for device_name, device in inputs.items():
            for cpu_name, cpu in device["schedule"].items():
                if len(cpu) > 0:
                    tasks_to_execute = True
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
                        executable_tasks.append([device_name, cpu_name, task_name])
                    else:
                        cpu.insert(0, task_name)

        # NOTE: Since we assume here that each task executes for the same
        # duration, run all of them at once. We'll generate outputs in the
        # execution model.
        step = {
            "timestep": outputs["next_timestep"],
            "started_tasks": {},
            "ending_tasks": {},
        }

        for device_name, cpu_name, task_name in executable_tasks:
            step["started_tasks"][device_name] = {cpu_name: (task_name, 1)}
            step["ending_tasks"][device_name] = {cpu_name: (task_name, 1)}

        outputs["steps"][outputs["next_timestep"]] = step
        outputs["next_timestep"] = step["timestep"] + 1

        return tasks_to_execute

    def get_model_name():
        return "ApplicationTimingModel_V0_0"
