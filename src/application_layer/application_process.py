"""_summary_
@file       application_process.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models a process on a device.
@version    0.0.0
@date       2022-10-16
"""


class ApplicationProcess:
    """_summary_
    Application layer processes execute a series of tasks that run when the
    process is active.
    """

    def __init__(self, process_name="DEFAULT_PROCESS"):
        """_summary_
        An application process simply consists of a series of tasks represented
        as a doubly linked list. This could be represented as a KPN (Kahn
        Process Network), except that the process is superset of the KPN instead
        of the actual KPN. Each individual task may fire outputs that are shared
        resources that may be obtained by other processes and tasks in the
        larger network.

        Args:
            process_name (str): The process name. Defaults to "DEFAULT_PROCESS".
        """
        self.tasks = []
        self.current_task_idx = 0
        self.process_runtime = 0
        self.process_name = process_name

    def add_task(self, task):
        if len(self.tasks) == 0:
            task.set_preceding_task(None)
            task.set_following_task(None)
        else:
            task.set_preceding_task(self.tasks[-1])
            self.tasks[-1].set_following_task(task)
        self.tasks.append(task)

    def add_loop(self):
        self.tasks[0].set_preceding_task(self.tasks[-1])
        self.tasks[-1].set_following_task(self.tasks[0])

    def get_task_list(self):
        return self.tasks

    def get_current_task(self):
        return self.tasks[self.current_task_idx]

    def get_process_name(self):
        return self.process_name

    def run_process(self, clock_cycles, resources):
        """_summary_
        Runs the process for an arbitrary duration.

        Args:
            clock_cycles (int): Number of clock cycles to run for.
            resources (dict): Resources available for the process to execute.
        """
        task = self.get_current_task()
        [is_task_completed, outputs] = task.run_task(clock_cycles, resources)
        self.process_runtime += clock_cycles

        if is_task_completed:
            # Move to the next task in the process.
            next_task = task.get_following_task()
            if next_task is None:
                # Is process completed? Is the task completed? What are the outputs?
                return [True, is_task_completed, outputs]
            else:
                self.current_task_idx = (self.current_task_idx + 1) % len(self.tasks)
                return [False, is_task_completed, outputs]
        else:
            return [False, is_task_completed, outputs]

    def clear_runtime(self):
        self.process_runtime = 0

    def get_process_runtime(self):
        """_summary_
        Returns the process runtime of the pinned process. 0 if just pinned.

        Returns:
            int: Returns the process runtime in ms.
        """
        return self.process_runtime
