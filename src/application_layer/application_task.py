"""_summary_
@file       application_task.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models a task with a process.
@version    0.0.0
@date       2022-10-16
"""


class ApplicationTask:
    """_summary_
    Application layer tasks consists of a series of instructions (steps) that
    modify the state of the device.

    They may require a set of inputs in order to execute and after executing,
    they generate a set of outputs. Each task also consists of a fixed duration.

    The application task can be modeled as a node in a Kahn process network.
    Tasks block until resource dependencies are fulfilled and the preceding task
    has finished firing.
    """

    def __init__(self, inputs={}, duration=1, outputs=[], task_name="DEFAULT_TASK"):
        """_summary_
        An application task has at least the following:
        - a set of inputs required to fire
        - a fire duration, in clock cycles
        - a set of outputs generated after firing

        Args:
            inputs (dict): A dict of inputs, where each key is paired with a
            number of relevant inputs that must be available for the task to
            fire. e.g.: {key: 4, door: 1} -> we need 4 keys and 1 door to fire
            the task, which could be opening the door.
            duration (int): How long it would take to fire the task in clock
            cycles when input dependencies are fulfilled.
            outputs (dict): A list of outputs generated by the task upon
            completion.
            task_name (str): The task name. Defaults to "DEFAULT_TASK".
        """
        self.inputs = inputs
        self.resources = {}
        for key in self.inputs.keys():
            self.resources[key] = []

        self.task_duration = duration
        self.task_remaining_duration = duration

        self.outputs = {}
        for key in outputs:
            self.outputs[key] = []

        self.task_name = task_name

    def is_executable(self, resources):
        """_summary_
        Check if the task is executable by comparing available resources against
        required dependencies.

        Args:
            resources (dict): A dict of available resources visible to the task.

        Returns:
            bool: True if the task can be executed. False otherwise.
        """

        if self.inputs is None:
            return False

        # Check resources against inputs.
        for [input_id, num_input_values] in self.inputs.items():
            if input_id in resources:
                if len(resources[input_id]) < num_input_values:
                    return False
            else:
                return False
        return True

    def run_task(self, clock_cycles, resources):
        """_summary_
        Execute transformation of inputs to generate the set of outputs. Task
        dependent code belongs here. Any amount of each input in self.inputs may
        be utilized to generate a subset of self.outputs.

        Args:
            resources (dict): Resource dict with input dependencies.
            clock_cycles (int): Number of clock cycles to run for.
        """
        # Consume inputs from resources.
        for [input_id, num_input_values] in self.inputs.items():
            for i in range(num_input_values):
                self.resources[input_id].append(resources[input_id].pop(0))

        # Generate outputs based on inputs.
        self.outputs["key"].append(self.resources["key"].pop(0) + 1)

        self.task_remaining_duration -= clock_cycles

        if self.task_remaining_duration > 0:
            return [False, None]
        else:
            return [True, self.outputs]

    def set_preceding_task(self, task):
        self.preceding_task = task

    def get_preceding_task(self):
        return self.preceding_task

    def set_following_task(self, task):
        self.following_task = task

    def get_following_task(self):
        return self.following_task

    def get_task_name(self):
        return self.task_name

    def get_duration(self):
        return self.task_duration

    def get_remaining_duration(self):
        return self.task_remaining_duration

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs
