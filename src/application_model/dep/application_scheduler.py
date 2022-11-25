"""_summary_
@file       application_scheduler.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Schedules processes for a device.
@version    0.0.0
@date       2022-10-16
"""
import copy


class ApplicationScheduler:
    """_summary_
    Application devices use schedulers, which control how processes are pinned
    to cores and how to resolve dependencies. There are many types of schedulers.
    """

    def __init__(self):
        pass

    def schedule_processes(self, processes=[], resources={}):
        """_summary_
        Dumb scheduler that may be implemented by the user in different flavors.
        We take a list of processes we want to run and a list of resources that
        are necessary to determine if the processes can be run, including the
        CPUs/cores on the device. The current scheduling algorithm is EDF with
        come, first serve. Cannot check for deadlocks.

        Args:
            processes (list, optional): Processes to schedule. Defaults to [].
            This reference is cleared of processes being utilized.
            resources (dict, optional): Resources to determine scheduling. Defaults to {}.

        Returns:
            list : A list of tuples consisting of the core ID and the process
            pinned to that core.
        """
        if "cores" not in resources:
            return []

        if len(processes) == 0:
            return []

        # Make a list of cores.
        free_cores = []
        busy_cores = []
        cores = resources["cores"]
        for core in cores:
            if core.get_pinned_process() is None:
                free_cores.append(core)
            else:
                busy_cores.append(core)

        # Get subset of processes whose dependencies are fulfilled by available
        # resources.
        runnable_processes = []
        for process in processes:
            current_task = process.get_current_task()
            executable = current_task.is_executable(resources)
            if executable:
                runnable_processes.append(process)

        # Sort by EDF (Earliest deadline first)
        def edf(runnable_process):
            return runnable_process.get_current_task().get_remaining_duration()

        runnable_processes.sort(key=edf)

        resource_copy = copy.deepcopy(resources)

        def consume_resources(inputs, resources):
            for [input_key, num_to_consume] in inputs.items():
                for i in range(num_to_consume):
                    resources[input_key].pop(0)

        # Assign processes to available cores while revalidating whether the
        # remaining processes have resources to them.
        for core in free_cores:
            for process in runnable_processes:
                executable = process.get_current_task().is_executable(resource_copy)
                if executable:
                    core.pin_process(process)
                    # Consume resources as dictated by dependencies.
                    consume_resources(
                        process.get_current_task().get_inputs(), resource_copy
                    )

                    # Remove process from consideration.
                    # Assume our pinned process always exsits in the list of
                    # processes. Otherwise we'll die through valueerror. Likely
                    # not multithreaded/multiprocess safe.
                    idx = processes.index(process)
                    processes.pop(idx)
                    break

        # Merge free and running cores and return the new list
        self.cores = free_cores + busy_cores
        return self.cores

    def get_schedule(self):
        return self.cores
