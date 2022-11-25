"""_summary_
@file       application_model_v0.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models device applications on a logical time ordering.
@version    0.0.0
@date       2022-11-23
"""

import copy
import pprint
import sys

from application_model_interface import ApplicationModelInterface


class ApplicationModel_V0_0(ApplicationModelInterface):
    """_summary_
    ApplicationModel_V0_0 models a very abstract interpretation of the NoS. It has
    following characteristics:
    - timing is event driven and the model evaluates devices and device tasks
      when an event starts or finishes.
    - hardware is given a static idle and active energy consumption value, which
      is used for determining eneryg usage over time.
    - transmission of data between devices is instantaneous and data is
      represented as a single communication.
    - a device has a static power source that provides a maximum fixed amount of
      energy at any moment.

    NOTE: V1.1 (Application expansion 1) has the following characteristics:
    - device schedules are ordered by some fixed time resolution.
    - device tasks can take more than one cycle to execute.
    - device cores have a core frequency
    - the model evaluates devices at each time step.

    NOTE: V1.3 (Energy expansion 1) has the following characteristics:
    - the power source has voltage and current characteristics within some
      distribution
    - multiple devices can share a single power source

    NOTE: V1.2 (Network expansion 1) has the following characteristics:
    - devices have a physical location in space
    - transmission of data is dependent based on distance between devices
    """

    def __init__(self) -> None:
        super().__init__()

    def add_device(self, device_name, device) -> bool:
        """_summary_
        Adds a device to the application model. A device must have the following
        attributes: 
        - device name (str)
        - a logical position consisting of a list of other devices that may or
          may not exist with which the device connects to (list(str))
        - a set of cores and hardware peripherals, each with:
            - a static idle and active energy consumption value (float, float)
        - a logically ordered scheduling and partitioning scheme for each core
          the device where each task:
            - specifies the input dependencies and output results.

        Args:
            device_name (_type_): _description_
            device (_type_): _description_

        Returns:
            bool: _description_
        """

        # TODO: verify that device has the above attributes.

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
                "devices": {
                },
                "cache": []
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
                                if dependency not in device["cache"]:
                                    deps_fulfilled = False

                        if deps_fulfilled:
                            # Consume dependencies and post to event timeline.
                            for dependency in task["dependencies"]:
                                device["cache"].remove(dependency)

                            timeline_entry["devices"][device_id]["cores"][core_id] = task["task_name"]
                            timeline_entry["devices"][device_id]["hw"].extend(task["hw"])
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
        pass    # no need to fail because of missing dev dependency

    model = ApplicationModel_V0_0()

    device_0 = {
        "device_name": "device_0",
        "neighbors": [],
        "cores": {
            "core_0": {
                "active_power": 100, # Joules
                "idle_power": 10, # Joules
            }
        },
        "peripherals": {
            "comm_0": {
                "active_power": 20, # Joules
                "idle_power": 10, # Joules
            },
            "adc_0": {
                "active_power": 10, # Joules
                "idle_power": 1, # Joules
            }
        },
        "schedule": {
            "core_0": [
                {
                    "task_name": "task_0a",
                    "dependencies": [],
                    "outputs": {
                        "output_0a": ["device_0"],
                    },
                    "hw": ["adc_0", ],
                },
                {
                    "task_name": "task_0b",
                    "dependencies": ["output_0a"],
                    "outputs": {
                        "output_0b": ["device_0"],
                    },
                    "hw": ["comm_0", ],
                },
            ]
        },
        "cache": []
    }

    model.add_device(device_0["device_name"], device_0)
    event_timeline = model.generate_event_timeline()
    pprint.pprint(event_timeline)

