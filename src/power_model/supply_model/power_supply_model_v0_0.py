"""_summary_
@file       power_supply_model_v0_0.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models power supply for devices.
@version    0.0.0
@date       2022-12-10
"""

import json
import sys


class PowerSupplyModel_V0_0:
    """_summary_
    The power supply is a fixed wattage defined by the designer.
    """

    def __init__(self):
        pass

    def process(self, outputs, inputs, supply_inputs, app_outputs):
        # Get a list of power supplies used for each device.
        supply_list = {}
        for device_name, device in inputs.items():
            for supply_name in device["power_supply"]:
                if supply_name not in supply_list:
                    # NOTE: In this layer, we consult the supply power parameter
                    # specified by the designer.
                    supply_list[supply_name] = {
                        "supply_power": supply_inputs[supply_name]["supply_power"],
                        "consumers": [device_name],
                    }
                else:
                    supply_list[supply_name]["consumers"].append(device_name)

        print(supply_list)

        # Generate a step list indicating the power available per device from
        # supply. Subtract power consumed by other devices on the same supply.
        outputs["producers"] = {}

        for step_idx, step in app_outputs["steps"].items():
            supplies = []
            # Check if no consumers are active. We want to leave the last entry
            # empty.
            if len(outputs["consumers"][step_idx]) > 0:
                for supply_name, supply in supply_list.items():
                    supply_consumer = []
                    supply_power = supply["supply_power"]
                    for device_name in supply["consumers"]:
                        consumers = [
                            consumer
                            for consumer in outputs["consumers"][step_idx]
                            if consumer[0] is not device_name
                        ]
                        if len(consumers) > 0:
                            consumed_power = 0
                            for consumer_name, consumer_power_usage in consumers[0][1]:
                                consumed_power += consumer_power_usage
                            supply_power -= consumed_power
                        supply_consumer.append((device_name, supply_power))
                    supplies.append([supply_name, supply_consumer])

                outputs["producers"][step_idx] = supplies

    def get_model_name(self):
        return "PowerSupplyModel_V0_0"
