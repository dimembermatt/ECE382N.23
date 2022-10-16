"""_summary_
@file       application_core.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models a CPU core for a device.
@version    0.0.0
@date       2022-10-16
"""


class ApplicationCore:
    """_summary_
    Application cores contain information about the CPU core and how it may
    operate. This includes information about expected power usage and speed.
    """

    core_id = 0

    def __init__(
        self,
        core_info={
            "clock_speed_hz": 1,
        },
    ):
        """_summary_
        An application core has at least the following:
        - core frequency: this may be a modifier that determines how long it
          to run a process or task of some duration. Fast clock speeds mean that
          the tasks can execute and finish earlier. Vice versa.

        Args:
            core_info (dict, optional): Core information. Defaults to {"clock_speed_hz": 1,}.
        """
        self.core_info = core_info
        self.pinned_process = None

        self.core_id = ApplicationCore.core_id
        ApplicationCore.core_id += 1

    def pin_process(self, process):
        """_summary_
        Pins the process on the core if it does not already have a pinned
        process. Call unpin_process() to unpin the current process, if any.

        Args:
            process (ApplicationProcess): Process to pin on the core.

        Returns:
            Bool: True if process can be pinned (no existing process)
        """
        if self.pinned_process is not None:
            return False
        else:
            self.pinned_process = process
            self.pinned_process.clear_runtime()
            return True

    def unpin_process(self):
        """_summary_
        Unpins the process on the core if it has a pinned process.
        """
        if self.pinned_process is not None:
            self.pinned_process = None

    def get_pinned_process(self):
        """_summary_
        Returns the process pinned to the core. None if no process.

        Returns:
            ApplicationProcess: Returns the pinned process, if any. Otherwise it
            a None.
        """
        return self.pinned_process

    def run_core(self, run_time, resources):
        """_summary_
        Runs the core for an arbitrary duration.

        Args:
            run_time (int): Time, in undefined units, to run the core for.
            TODO: specify units
            resources (dict): Reference to device resources that can be consumed
            the device.
        """
        if self.pinned_process is None:
            return [True, {}]

        # Run the process for an arbitrary amount of time. Given the device
        # core_info, we can translate this time into clock cycles.
        clock_cycles = self.convert_time_to_clock_cycles(run_time)

        [
            is_process_completed,
            is_task_completed,
            outputs,
        ] = self.pinned_process.run_process(clock_cycles, resources)

        # Unpin the process if we're completed.
        if is_process_completed:
            self.unpin_process()

        return [is_process_completed, is_task_completed, outputs]

    def convert_time_to_clock_cycles(self, time):
        """_summary_

        Args:
            time (int): time in ms.

        Returns:
            int: Number of clock cycles that can be executed.
        """
        return time * self.core_info["clock_speed_hz"] / 1000

    def convert_clock_cycles_to_time(self, clock_cycles):
        return clock_cycles * 1000 / self.core_info["clock_speed_hz"]

    def get_core_id(self):
        return self.core_id
