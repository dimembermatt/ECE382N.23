"""_summary_
@file       application_hardware_model_v0_0.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models hardware interactions for each task.
@version    0.0.0
@date       2022-12-11
"""


class ApplicationHardwareModel_V0_0:
    """_summary_
    Tasks generate a set of hardware that is executed for their duration. These
    hardware peripherals are assumed to be constantly active for the duration
    of the task.
    """

    def __init__(self):
        pass

    def process_step(self, outputs, inputs):
        # Get the current step
        step = [
            list(outputs["steps"].keys())[-1],
            outputs["steps"][list(outputs["steps"].keys())[-1]],
        ]

        step[1]["active_peripherals"] = {}

        # For each task in each device and cpu, generate the hardware used.
        for device_name, device in step[1]["started_tasks"].items():
            hardware_used = set()
            for cpu_name, (task_name, task_duration, data) in device.items():
                for hardware in inputs[device_name]["tasks"][task_name]["hardware"]:
                    hardware_used.add(hardware)

            step[1]["active_peripherals"][device_name] = list(hardware_used)

    def get_model_name(self):
        return "ApplicationHardwareModel_V0_0"
