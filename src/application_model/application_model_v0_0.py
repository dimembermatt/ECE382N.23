"""_summary_
@file       application_model_v0_0.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models device applications.
@version    0.0.0
@date       2022-11-28
"""

import copy
import sys

from application_model_interface import ApplicationModelInterface


class ApplicationModel_V0_0(ApplicationModelInterface):
    """_summary_
    ApplicationModel_V0_0 models a very abstract interpretation of the NoS. It
    has the following characteristics:
    - timing is event driven and the model evaluates devices and device tasks
      when an event starts or finishes.
    """

    def __init__(self) -> None:
        super().__init__("V0_0 Application Model")

    def add_device(self, device_name, device) -> bool:
        """_summary_
        Adds a device to the application model. A device must have the following
        attributes:
        - device name (str)
        - a logically ordered scheduling and partitioning scheme for a number of
          cores on the device where each task:
            - specifies the input dependencies and output results.

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

        # While we still have tasks available for each device schedule
        timestamp = 0
        while True:
            timeline_complete = True
            timeline_entry = {
                "timestamp": timestamp,
                "duration": 1,
                "devices": {},
                "cache": [],
            }

            # Go through each device's schedule, look at the first task
            # If the first task has no remaining dependencies, pop from schedule
            # and add to tasks. Do this for all tasks that can execute
            # immediately.
            for device_id, device in devices.items():
                timeline_entry["devices"][device_id] = {
                    "cores": {},
                    "hw": [],
                }

                for core_id, core in device["schedule"].items():
                    if len(core) > 0:
                        task = core[0]

                        deps_fulfilled = True
                        if len(task["dependencies"]) > 0:
                            for dependency in task["dependencies"]:
                                if "cache" not in device:
                                    device["cache"] = []
                                if dependency not in device["cache"]:
                                    deps_fulfilled = False

                        if deps_fulfilled:
                            # Consume dependencies and post to event timeline.
                            for dependency in task["dependencies"]:
                                device["cache"].remove(dependency)

                            timeline_entry["devices"][device_id]["cores"][
                                core_id
                            ] = task["task_name"]
                            timeline_entry["devices"][device_id]["hw"].extend(
                                task["hw"]
                            )
                            timeline_entry["cache"].append(task["outputs"])
                            del core[0]

                    # Check if we've removed everything from this device core's schedule
                    if len(core) > 0:
                        timeline_complete = False

            # Now that all outputs have been posted to the entry, stash back
            # into the cache of the devices for the next round.
            for output_dict in timeline_entry["cache"]:
                for output_id, output_targets in output_dict.items():
                    for output_target in output_targets:
                        if "cache" not in devices[output_target]:
                            devices[output_target]["cache"] = [output_id]
                        else:
                            devices[output_target]["cache"].append(output_id)

            self._event_timeline.append(timeline_entry)
            timestamp += 1
            if timeline_complete:
                break

        return super().generate_event_timeline()


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    try:
        import pretty_traceback

        pretty_traceback.install()
    except ImportError:
        pass  # no need to fail because of missing dev dependency

    model = ApplicationModel_V0_0()

    device_0 = {
        "device_name": "device_0",
        "cores": {"core_0": {}},
        "schedule": {
            "core_0": [
                {
                    "task_name": "task_A",
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
        "cores": {"core_0": {}, "core_1": {}},
        "schedule": {
            "core_0": [
                {
                    "task_name": "task_AA",
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
                {
                    "task_name": "task_AA",
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
                {
                    "task_name": "task_C",
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
                    "dependencies": [],
                    "outputs": {},
                    "hw": [],
                },
                {
                    "task_name": "task_E",
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
                    "dependencies": ["output_2"],
                    "outputs": {
                        "output_3": ["device_1"],
                    },
                    "hw": [],
                },
                {
                    "task_name": "task_G",
                    "dependencies": ["output_3"],
                    "outputs": {
                        "output_4": ["device_1"],
                    },
                    "hw": [],
                },
                {
                    "task_name": "task_H",
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
    model.save_outputs()
    model.visualize_event_timeline()
