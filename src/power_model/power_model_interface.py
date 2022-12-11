"""_summary_
@file       power_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device power
            consumption.
@version    0.0.0
@date       2022-12-11
"""


import json
import sys

import matplotlib.pyplot as plt
from colorhash import ColorHash

from power_model.consumption_model.power_consumption_model_v0_0 import (
    PowerConsumptionModel_V0_0,
)
from power_model.consumption_model.power_consumption_model_v0_1 import (
    PowerConsumptionModel_V0_1,
)
from power_model.supply_model.power_supply_model_v0_0 import PowerSupplyModel_V0_0


def get_power_consumption_models(consumption_model_str):
    match consumption_model_str:
        case "PowerConsumptionModel_V0_0":
            # Power consumption is dictated by idle and active power consumption.
            return PowerConsumptionModel_V0_0()
        case "PowerConsumptionModel_V0_1":
            # Power consumption is dictated by device voltage and idle and
            # current consumption.
            return PowerConsumptionModel_V0_1()
        case "PowerConsumptionModel_V0_2":
            # TODO: PowerConsumptionModel_V0_2
            # Power consumption is dictated by a voltage and current
            # distribution.
            return None
        case "PowerConsumptionModel_V0_3":
            # TODO: PowerConsumptionModel_V0_3
            # Power consumption is dicted by a power function whose inputs are
            # the processor frequency, processor task function and dependencies,
            # as well as hardware used.
            return None
        case _:
            return None


def get_power_supply_models(supply_model_str):
    match supply_model_str:
        case "PowerSupplyModel_V0_0":
            # Power available is dictated by a power generation parameter.
            return PowerSupplyModel_V0_0()
        case "PowerSupplyModel_V0_1":
            # TODO: PowerSupplyModel_V0_1
            # Power available is dictated by a power generation distribution
            # parameter.
            return None
        case "PowerSupplyModel_V0_2":
            # TODO: PowerSupplyModel_V0_2
            # Power available is dictated by voltage, current, and conversion
            # efficiency.
            return None
        case "PowerSupplyModel_V0_3":
            # TODO: PowerSupplyModel_V0_3
            # Power available is dictated by voltage, current, and conversion
            # efficiency distributions.
            return None
        case "PowerSupplyModel_V0_4":
            # TODO: PowerSupplyModel_V0_4
            # Power available is dictated by a user defined power function whose
            # inputs are current power load.
            return None
        case _:
            return None


class PowerModelInterface:
    def __init__(
        self,
        path,
        device_inputs,
        supply_inputs,
        app_outputs,
        consumption_model_str,
        supply_model_str,
    ):
        sys.path.append(path)
        self.path = path
        self.consumption_model = get_power_consumption_models(consumption_model_str)
        self.supply_model = get_power_supply_models(supply_model_str)
        self.inputs = device_inputs
        self.supply_inputs = supply_inputs
        self.app_outputs = app_outputs
        self.outputs = {"consumers": None, "producers": None}

        print("Running the following power submodel sub-submodels:")
        print(f"\t-Consumption Model: {self.consumption_model.get_model_name()}")
        print(f"\t-Supply Model: {self.supply_model.get_model_name()}")

    def generate_output(self):
        self.consumption_model.process(self.outputs, self.inputs, self.app_outputs)
        self.supply_model.process(
            self.outputs, self.inputs, self.supply_inputs, self.app_outputs
        )

        plt.figure(1)
        fig = plt.gcf()
        fig.set_size_inches(10, 5, forward=True)
        fig.suptitle("Power Usage")

        num_devices = len(self.inputs.keys())
        axs = {}
        for idx, device_name in enumerate(self.inputs.keys()):
            axs[device_name] = fig.add_subplot(num_devices, 1, idx + 1)
            axs[device_name].set_xlabel("Timestep (cycles)")
            axs[device_name].set_ylabel("Power Usage (W)")
            axs[device_name].set_title(
                f"Device {device_name} Power Consumption Over Time"
            )

        # Plot consumer broken bar graphs
        for step_idx, step in self.outputs["consumers"].items():
            for device_name, consumers in step:
                ax = axs[device_name]
                y = 0
                for consumer_name, consumer_power_consumption in consumers:
                    c = [x / 255 for x in ColorHash(consumer_name).rgb]
                    current_time = self.app_outputs["steps"][step_idx]["timestep"]
                    duration = self.app_outputs["steps"][step_idx]["duration"]
                    ax.bar(
                        [current_time + duration / 2],
                        [consumer_power_consumption],
                        bottom=y,
                        width=duration,
                        label=f"{consumer_name}",
                        color=[*c],
                    )
                    ax.text(
                        x=current_time + duration / 2,
                        y=y + consumer_power_consumption / 2,
                        s=f"{consumer_name}",
                        ha="center",
                        va="center",
                        color="black",
                    )
                    y += consumer_power_consumption

        print(json.dumps(self.outputs, indent=4))
        # Plot producers line
        for step_idx, step in self.outputs["producers"].items():
            for supply_name, consumers in step:
                for device_name, available_power in consumers:
                    ax = axs[device_name]
                    c = [x / 255 for x in ColorHash(device_name).rgb]
                    current_time = self.app_outputs["steps"][step_idx]["timestep"]
                    duration = self.app_outputs["steps"][step_idx]["duration"]
                    ax.plot(
                        [current_time, current_time + duration],
                        [available_power] * 2,
                        c=c,
                    )

        return self.outputs

    def print_outputs(self):
        print(json.dumps(self.outputs, indent=4))

    def pprint_outputs(self):
        # TODO: generate pretty print output format.
        pass

    def visualize_power_usage(self):
        plt.show()

    def save_outputs(self):
        plt.figure(1)
        plt.tight_layout()
        fig = plt.gcf()
        fig.savefig(f"{self.path}output_power_usage.png", dpi=100)
        with open(f"{self.path}output_power_usage.json", "w") as fp:
            json.dump(self.outputs, fp, indent=4)
