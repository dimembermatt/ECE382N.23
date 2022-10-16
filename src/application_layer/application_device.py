"""_summary_
@file       application_device.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models a particular device in the application layer.
@version    0.0.0
@date       2022-10-16
"""

from application_layer.application_core import ApplicationCore
from application_layer.application_scheduler import ApplicationScheduler


class ApplicationDevice:
    """_summary_
    Application layer devices manage a set of processes on the device, as well
    as abstract representations of the hardware associated with the device, such
    as sensor attachments, storage, and transceivers. Each application layer
    device has a set of 'specs' that determine the functionality and performance
    of the processes on the device.

    Devices may have schedulers that operate on their individual processes.
    """

    device_id = 0

    def __init__(
        self, resources={"cores": [ApplicationCore()]}, scheduler=ApplicationScheduler()
    ):
        """_summary_
        An application device has at least the following:
         - Hardware resources, including CPUs, ADCs, DACs, transceivers, etc
         - Software scheduler for determining how processes run on the hardware.

        Args:
            resources (dict, optional): Hardware resources available. Defaults
            to {"cores": ApplicationCore()}.
            scheduler (_type_, optional): Software scheduler used. Defaults to
            ApplicationScheduler().
        """
        self.processes = []
        self.resources = resources
        self.scheduler = scheduler

        self.device_id = ApplicationDevice.device_id
        ApplicationDevice.device_id += 1

    def add_process(self, process):
        """_summary_
        Queues a process on the device.

        Args:
            process (ApplicationProcess): Adds a process that must be executed.
        """
        self.processes.append(process)

    def add_resource(self, resource_id, resource_value):
        """_summary_
        Adds a resource of a given key to the device.

        Args:
            resource_id (key): Dict key.
            resource_value (list): list of values that need to be added.
        """
        if resource_id in self.resources:
            self.resources[resource_id].extend(resource_value)
        else:
            self.resources[resource_id] = resource_value

    def get_processes(self):
        """_summary_
        Get active or queued processes on the device.

        Returns:
            list: Process list of active or queued processes.
        """
        return self.processes

    def get_resources(self):
        """_summary_
        Get a keyed dict of resources available on the device. This could
        include information such as CPU/core information, peripherals, and so
        forth.

        Returns:
            dict: Keyed dict of resources on device.
        """
        return self.resources

    def get_scheduler(self):
        """_summary_
        Get the scheduler instance used to schedule processes on the device.

        Returns:
            ApplicationScheduler: An instance of a scheduler used on the device.
        """
        return self.scheduler

    def schedule(self):
        """_summary_
        Tells our internal scheduler to schedule processes.
        """
        schedule = self.scheduler.schedule_processes(self.processes, self.resources)
        return schedule

    def run_device(self, run_time):
        """_summary_
        Runs the device for an arbitrary duration.

        Args:
            run_time (int): Time, in undefined units, to run the device for.
            TODO: specify units
        """
        if "cores" in self.resources:
            for core in self.resources["cores"]:
                [is_process_completed, is_task_completed, outputs] = core.run_core(
                    run_time, self.resources
                )
                # If the current task is done, merge outputs back into device resources.
                if is_task_completed:
                    for [resource_id, resource_value] in outputs.items():
                        # TODO: add support for resources that must be routed to
                        # other layers.
                        self.add_resource(resource_id, resource_value)
                # If the current process is done, reschedule the core.
                if is_process_completed:
                    self.schedule()
        else:
            raise Exception("NO CORES SPECIFIED FOR DEVICE")

    def get_device_id(self):
        return self.device_id
