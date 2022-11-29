"""_summary_
@file       application_model_v0_1.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models device applications.
@version    0.0.0
@date       2022-11-28
"""

import copy
import sys

from application_model_interface import ApplicationModelInterface


class ApplicationModel_V0_1(ApplicationModelInterface):
    """_summary_
    ApplicationModel_V0_1 (Application expansion 1) models a very abstract
    interpretation of the NoS. It has the following characteristics:
    - device schedules are ordered by some fixed time resolution.
    - device tasks can take more than one cycle to execute.
    - device cores have a core frequency that affect execution time.
    - the model evaluates devices at each time step.
    """

    def __init__(self) -> None:
        super().__init__("V0_1 Application Model")

    def add_device(self, device_name, device) -> bool:
        """_summary_
        Adds a device to the application model. A device must have the following
        attributes:
        - device name (str)
        - core frequencies for each core (int)
        - a temporally ordered scheduling and partitioning scheme for a number
          of cores on the device where each task:
            - specifies the input dependencies and output results.
            - has a fixed duration in cycles

        Args:
            device_name (_type_): _description_
            device (_type_): _description_

        Returns:
            bool: _description_
        """
        return super().add_device(device_name, device)

    def generate_event_timeline(self) -> dict:
        """_summary_
        {
            "device_0": {
                "cores": {
                    "core_0": {
                        "frequency": 1,
                    }, ...
                }
                "schedule": {
                    "core_0": [{
                        "task_name": task_0a,
                        "dependencies": [None],
                        "outputs": {
                            "output_0a": ["device_1"] <- send output_0a to device_1
                        },
                        "hw": ["adc_0", "comm_0", ... ]
                    }, ... ],
                    "core_1": [ ... ],
                }
            },
            "device_1: { ... }
        }
        """

        devices = copy.deepcopy(self._devices)

        # TODO: I hate this, please clean up future me
        running_devices = {}
        timestamp = 0
        while True:
            timeline_entry = {
                "timestamp": timestamp,
                "duration": 0,
                "devices": {},
                "cache": []
            }

            # Devices with active tasks keep running in the next iteration.
            if len(running_devices.keys()) != 0:
                timeline_entry["devices"].update(running_devices)

            # For each device, check to see if it can run
            for device_id, device in devices.items():
                device_entry = {"cores": {}, "hw": []}

                # For each core, check to see if there are any available tasks
                for core_id, core in device["schedule"].items():
                    # If core is currently running something else
                    if (
                        device_id in timeline_entry["devices"]
                        and core_id in timeline_entry["devices"][device_id]["cores"]
                    ):
                        continue
                    # Core has tasks available for us
                    elif len(core) > 0:
                        task = core[0]

                        # Am I waiting on any dependencies?
                        deps_fulfilled = True
                        if len(task["dependencies"]) > 0:
                            for dependency in task["dependencies"]:
                                if "cache" not in device:
                                    device["cache"] = []
                                if dependency not in device["cache"]:
                                    deps_fulfilled = False

                        # If not, post the core to the event timeline.
                        # "Start execution".
                        if deps_fulfilled:
                            # Consume the task dependencies.
                            for dependency in task["dependencies"]:
                                device["cache"].remove(dependency)

                            # Generate the device entry.
                            device_entry["cores"][core_id] = {
                                "core_freq": device["cores"][core_id]["frequency"],
                                "task": task["task_name"],
                                "task_duration": task["duration"],
                                "cache": task["outputs"],
                            }

                            # Any HW used during this task execution, add to
                            # the device entry.
                            device_entry["hw"].extend(task["hw"])

                            # Remove task from the device.
                            del core[0]

                    if device_id not in timeline_entry["devices"]:
                        timeline_entry["devices"][device_id] = device_entry

            # Look at all tasks and order them by end time.
            tasks = []
            for device_id, device in timeline_entry["devices"].items():
                for core_id, core in device["cores"].items():
                    duration = core["task_duration"] / core["core_freq"]
                    task = {
                        "device_id": device_id,
                        "core_id": core_id,
                        "task_id": core["task"],
                        "duration": duration,
                    }
                    tasks.append(task)

            if len(tasks) > 0:

                def get_duration(elem):
                    return elem["duration"]

                tasks.sort(key=get_duration)
                duration = tasks[0]["duration"]
                timeline_entry["duration"] = duration

                # "Execute" the first N tasks with the shortest duration.
                done_tasks = []
                remaining_tasks = []
                for task in tasks:
                    if task["duration"] == duration:
                        done_tasks.append(task)
                    else:
                        remaining_tasks.append(task)

                # For the tasks that have "executed", send outputs to cache.
                for task in done_tasks:
                    device_id = task["device_id"]
                    core_id = task["core_id"]
                    outputs = timeline_entry["devices"][device_id]["cores"][core_id][
                        "cache"
                    ]

                    # Output to main cache.
                    timeline_entry["cache"].append(outputs)

                    # Update individual device cache.
                    for output_id, output_targets in outputs.items():
                        for output_target in output_targets:
                            if "cache" not in devices[output_target]:
                                devices[output_target]["cache"] = [output_id]
                            else:
                                devices[output_target]["cache"].append(output_id)

                # Advance time by the duration of the shortest tasks.
                timestamp += duration

                # Propagate remaining tasks to the next timeline_entry.
                running_devices = {}
                for task in remaining_tasks:
                    device_id = task["device_id"]
                    core_id = task["core_id"]
                    core = timeline_entry["devices"][device_id]["cores"][core_id]
                    core["task_duration"] -= duration

                    if device_id in running_devices:
                        running_devices[device_id]["cores"][core_id] = copy.deepcopy(
                            core
                        )
                        running_devices[device_id]["hw"] = copy.deepcopy(
                            timeline_entry["devices"][device_id]["hw"]
                        )
                    else:
                        running_devices[device_id] = {
                            "cores": {core_id: copy.deepcopy(core)},
                            "hw": copy.deepcopy(
                                timeline_entry["devices"][device_id]["hw"]
                            ),
                        }

                # Reformat each core entry to just contain the task name.
                for device_id, device in timeline_entry["devices"].items():
                    for core_id, core in device["cores"].items():
                        timeline_entry["devices"][device_id]["cores"][
                            core_id
                        ] = timeline_entry["devices"][device_id]["cores"][core_id][
                            "task"
                        ]

                self._event_timeline.append(timeline_entry)
            else:
                return super().generate_event_timeline()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    try:
        import pretty_traceback

        pretty_traceback.install()
    except ImportError:
        pass  # no need to fail because of missing dev dependency

    model = ApplicationModel_V0_1()

    device_0 = {
        "device_name": "device_0",
        "cores": {"core_0": {"frequency": 1}},  # Hz,
        "schedule": {
            "core_0": [
                {
                    "task_name": "task_A",
                    "duration": 1,  # cycle
                    "dependencies": [],
                    "outputs": {
                        "output_0": ["device_0"],
                    },
                    "hw": [
                        "adc_0",
                    ],
                },
                {
                    "task_name": "task_B",
                    "duration": 1,  # cycle
                    "dependencies": ["output_0"],
                    "outputs": {
                        "output_1": ["device_1"],
                    },
                    "hw": [
                        "comm_0",
                    ],
                },
            ]
        },
        "cache": [],
    }

    device_1 = {
        "device_name": "device_1",
        "cores": {
            "core_0": {
                "frequency": 1,  # Hz
            },
            "core_1": {
                "frequency": 1,  # Hz
            },
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "task_AA",
                    "duration": 2,
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
                {
                    "task_name": "task_C",
                    "duration": 1,  # cycle
                    "dependencies": ["output_1"],
                    "outputs": {
                        "output_2": ["device_1"],
                    },
                    "hw": [
                        "comm_0",
                    ],
                },
                {
                    "task_name": "task_D",
                    "duration": 1,  # cycle
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
                {
                    "task_name": "task_E",
                    "duration": 1,  # cycle
                    "dependencies": ["output_5"],
                    "outputs": {
                        "output_7": ["device_1"],
                    },
                    "hw": [],
                },
            ],
            "core_1": [
                {
                    "task_name": "task_F",
                    "duration": 1,  # cycle
                    "dependencies": ["output_2"],
                    "outputs": {
                        "output_3": ["device_1"],
                    },
                    "hw": [],
                },
                {
                    "task_name": "task_G",
                    "duration": 1,  # cycle
                    "dependencies": ["output_3"],
                    "outputs": {
                        "output_4": ["device_1"],
                    },
                    "hw": [],
                },
                {
                    "task_name": "task_H",
                    "duration": 1,  # cycle
                    "dependencies": [],
                    "outputs": {
                        "output_5": ["device_1"],
                    },
                    "hw": [],
                },
            ],
        },
        "cache": [],
    }

    model.add_device(device_0["device_name"], device_0)
    model.add_device(device_1["device_name"], device_1)

    event_timeline = model.generate_event_timeline()
    print(event_timeline)
    model.print_event_timeline()
    model.visualize_event_timeline()
