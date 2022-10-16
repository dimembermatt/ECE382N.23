"""_summary_
@file       application_layer.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Manages the devices and processes in the model.
@version    0.0.0
@date       2022-10-12
"""

import sys
from operator import itemgetter

sys.path.append("../../src")


class ApplicationLayer:
    """_summary_
    The application layer consists of a set of devices, each of which contains
    individual processes. The application layer runs these devices in "parallel"
    and organizes their execution in arbitrary resolution and order. The
    application layer generates a timeline of events, which can be visually
    plotted, and passes information from devices and processes to other layers,
    such as the Network Layer and Energy Layer.
    """

    def __init__(self):
        self.devices = {}
        self.task_list = []
        self.time_stamp_ms = 0
        self.event_timeline = []

    def add_device(self, device_id, device):
        # Add a device to the application layer.
        self.devices[device_id] = device

    def print_event_timeline(self):
        # Generate the event timeline.
        entry = [self.time_stamp_ms, []]
        for device in self.devices.values():
            resources = device.get_resources()
            cores = resources["cores"]
            for core in cores:
                process = core.get_pinned_process()
                if process is None:
                    process_name = "NONE"
                    task_name = "NONE"
                    task_duration = 0
                else:
                    process_name = process.get_process_name()
                    task_name = process.get_current_task().get_task_name()
                    task_duration = core.convert_clock_cycles_to_time(
                        process.get_current_task().get_remaining_duration()
                    )

                sub_entry = (
                    "dev_" + str(device.get_device_id()),
                    "core_" + str(core.get_core_id()),
                    process_name,
                    task_name,
                    task_duration,
                )
            entry[1].append(sub_entry)

        self.event_timeline.append(entry)
        print(self.event_timeline)

    def initialize_layer(self):
        """_summary_
        Schedules the starting process for each device and generates an initial
        entry in the timeline for analysis.
        """
        self.task_list = []

        # Get all devices on the network
        devices = self.devices.values()

        # For each device, get their schedules
        for device in devices:
            cores = device.schedule()

            # Get the active process and therefore task
            for core in cores:
                process = core.get_pinned_process()
                task = process.get_current_task()
                self.task_list.append(
                    [
                        device,
                        core,
                        process,
                        task,
                        core.convert_clock_cycles_to_time(
                            task.get_remaining_duration()
                        ),
                    ]
                )

        # Order task by EDF
        sorted(self.task_list, key=itemgetter(4))

        self.print_event_timeline()

    def step_layer(self):
        """_summary_
        Runs the model one step (either logical or temporal).
        """
        task = self.task_list.pop(0)
        min_duration = task[4]

        self.time_stamp_ms += min_duration

        # Execute all tasks for the duration of the EDT.
        for device in self.devices.values():
            device.run_device(min_duration)

        # Regenerate task list with any new tasks.
        self.task_list = []

        # Get all devices on the network
        devices = self.devices.values()

        # For each device, get their schedules
        for device in devices:
            cores = device.get_scheduler().get_schedule()

            # Get the active process and therefore task
            for core in cores:
                process = core.get_pinned_process()
                if process is not None:
                    task = process.get_current_task()
                    self.task_list.append(
                        [
                            device,
                            core,
                            process,
                            task,
                            core.convert_clock_cycles_to_time(
                                task.get_remaining_duration()
                            ),
                        ]
                    )

        # Order task by EDF
        sorted(self.task_list, key=itemgetter(4))

        self.print_event_timeline()

    def get_event_timeline(self):
        return self.event_timeline
