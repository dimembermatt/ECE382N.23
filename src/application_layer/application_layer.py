"""_summary_
@file       application_layer.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Manages the devices and processes in the model.
@version    0.0.0
@date       2022-10-12
"""


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

    def add_device(self, device_id, device):
        # Add a device to the application layer.
        self.devices[device_id] = device

    def start(self):
        # TODO: return a list of scheduled processes and tasks across all
        # devices before they start.
        pass

    def step(self):
        # Run each device in parallel. Step through each device and retrieve
        # their inputs/outputs.
        for [device_id, device] in self.devices.items():
            device.schedule_process()
            device_result = device.step()
            # TODO: manage results, build dependencies

        # TODO: Communicate with other layers


class ApplicationDevice:
    """_summary_
    Application layer devices manage a set of processes on the device, as well
    as abstract representations of the hardware associated with the device, such
    as sensor attachments, storage, and transceivers. Each application layer
    device has a set of 'specs' that determine the functionality and performance
    of the processes on the device.

    Devices may have schedulers that operate on their individual processes.
    """

    def __init__(self, num_cores=1):
        self.processes = []
        self.cores = {}
        for core_idx in range(num_cores):
            self.cores[core_idx] = {"running_process": None, "process_run_time": None}
        # TODO: support for shared resources.

    def add_process(self, process):
        self.processes.append(process)

    def schedule_process(self):
        """_summary_
        Schedules the processes based on the available cores for the current
        time step. Device dependent code belongs here. By default, the scheduler
        is dumb and runs processes in order of attachment and does not multiplex
        between processes.
        """
        # TODO: develop dumb scheduler. If cores do not have a running process,
        # give it one. Processes are removed when complete by the step function.
        pass

    def step(self):
        """_summary_
        Executes a single step of the active processes and returns the output.
        """
        result = {
            "completed_processes": {},  # dict of processes that were completed, including their start times, finish times, and their inputs/outputs.
            "running_processes": {},
        }


class ApplicationProcess:
    """_summary_
    Application layer processes execute a series of tasks that run when the
    process is active.
    """

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if len(self.tasks) == 0:
            task.set_preceding_task(None)
            self.tasks.append(task)
        else:
            task.set_preceding_task(self.tasks[-1])
            self.tasks[-1].set_following_task(task)

        # TODO: figure out how to loop tasks.

    def add_loop(self):
        self.task[0].set_preceding_task(self.tasks[-1])
        self.task[-1].set_following_task(self.tasks[0])

    def get_task_list(self):
        return self.tasks


class ApplicationTask:
    """_summary_
    Application layer tasks consists of a series of instructions (steps) that
    consist of the following
    - an execution duration
    - a preceding task (if any)
    - a following task (if any)
    - resource dependencies created by the preceding tasks or by other
    application layer processes.

    The application task can be modeled as a node in a Kahn process network.
    Tasks block until resource dependencies are fulfilled and the preceding task
    has finished firing
    """

    def __init__(self, inputs, task_duration, outputs):
        self.inputs = {}
        self.task_duration = task_duration
        self.outputs = outputs

    def enter(self, inputs):
        """_summary_
        Pass inputs to the application task. May be called multiple times if
        necessary.

        Args:
            inputs (list): [[input_id, input_value], ...]
        """
        for input in inputs:
            if input[0] in self.inputs:
                self.inputs[input[0]].append(input[1])

    def is_executable(self):
        """_summary_

        Returns:
            bool: Return False if not all inputs have a ready data value. True
            otherwise.
        """
        if self.inputs is None:
            return False

        for input in self.inputs:
            if len(input) == 0:
                return False

        return True

    def execute(self):
        """_summary_
        Execute transformation of inputs to generate the set of outputs. Task
        dependent code belongs here. Any amount of each input in self.inputs may
        be utilized to generate a subset of self.outputs. By default, the
        execution generates no useful outputs given any inputs.
        """
        pass

    def exit(self):
        """_summary_

        Returns:
            list: A list of outputs.
        """
        # Build a list of outputs.
        outputs = []
        for (output_id, output_value) in self.outputs.items():
            outputs.append([output_id, output_value])

        # Clear out outputs.
        for output_id in self.outputs.keys():
            self.outputs[output_id] = None

        return outputs

    def set_preceding_task(self, task):
        self.preceding_task = task

    def get_preceding_task(self):
        if self.preceding_task is not None:
            return self.preceding_task
        return None

    def set_following_task(self, task):
        self.following_task = task

    def get_following_task(self):
        if self.following_task is not None:
            return self.following_task
        return None
