"""_summary_
@file       power_consumption_model_v0_1.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models power consumption of devices.
@version    0.0.1
@date       2022-12-11
"""


class PowerConsumptionModel_V0_1:
    """_summary_
    Hardware power consumption is determined by a voltage and current parameter.
    """

    def __init__(self):
        pass

    def process(self, outputs, inputs, app_outputs):
        # Get a list of hardware for each device.
        hardware_list = {}
        for device_name, device in inputs.items():
            hardware_list[device_name] = [
                hardware_name for hardware_name in device["hardware"].keys()
            ]

        # For each step in the app outputs, observe the started and running
        # tasks and evaluate active hardware and idle hardware.
        power_steps = {}
        for step_idx, step in app_outputs["steps"].items():
            power_step = {}
            for device_name, active_hardware in step["active_peripherals"].items():
                power_step[device_name] = {"active_hardware": active_hardware}
                idle_hardware = [
                    hardware_name
                    for hardware_name in hardware_list[device_name]
                    if hardware_name not in power_step[device_name]["active_hardware"]
                ]
                power_step[device_name]["idle_hardware"] = idle_hardware
            power_steps[step_idx] = power_step

        # Generate a step list indicating the power consumption per device
        # hardware sorted from largest to smallest.
        outputs["consumers"] = {}
        for step_idx, step in power_steps.items():
            devices = []
            for device_name, consumers in step.items():
                # NOTE: In this layer, we consult the active and idle power
                # consumption parameters specified by the designer.
                active_consumers = [
                    (
                        consumer_name,
                        inputs[device_name]["hardware"][consumer_name]["voltage"]
                        * inputs[device_name]["hardware"][consumer_name]["current"][1],
                    )
                    for consumer_name in consumers["active_hardware"]
                ]
                idle_consumers = [
                    (
                        consumer_name,
                        inputs[device_name]["hardware"][consumer_name]["voltage"]
                        * inputs[device_name]["hardware"][consumer_name]["current"][0],
                    )
                    for consumer_name in consumers["idle_hardware"]
                ]
                consumers = active_consumers + idle_consumers
                sorted(consumers, key=lambda x: x[1])
                devices.append([device_name, consumers])

            outputs["consumers"][step_idx] = devices

    def get_model_name(self):
        return "PowerConsumptionModel_V0_1"
