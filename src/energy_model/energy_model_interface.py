"""_summary_
@file       energy_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device energy usage.
@version    0.0.0
@date       2022-11-28
"""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from colorhash import ColorHash


class EnergyModelInterface:
    def __init__(self, model_name) -> None:
        self._devices = {}
        self._energy_supplies = {}
        self._energy_usage = []
        self._fig, self._ax = None, None
        self._model_name = model_name

    def add_device(self, device_name, device) -> bool:
        if device_name in self._devices:
            return False
        self._devices[device_name] = device
        return True

    def add_energy_supply(self, supply_name, supply) -> bool:
        if supply_name in self._energy_supplies:
            return False
        self._energy_supplies[supply_name] = supply
        return True

    def generate_energy_usage(self) -> dict:
        # Generate y components.
        self._fig, self._axs = plt.subplots(len(self._devices.keys()))

        if len(self._devices.keys()) > 1:
            for ax, device_id in zip(self._axs, self._devices.keys()):
                ax.set_xlabel("Time (cycles)")
                ax.set_ylabel("Energy Usage (J)")
                ax.set_title(f"Device {device_id} Energy Consumption Over Time")
                self._devices[device_id]["ax"] = ax
                # Print power limit line
                timestamps = []
                lastDuration = 0
                for event in self._energy_usage:
                    timestamps.append(event["timestamp"])
                    lastDuration = event["duration"]
                timestamps.append(timestamps[-1] + lastDuration)
                max_pwr = self._devices[device_id]["supply"]["supply_voltage"]*self._devices[device_id]["supply"]["max_supply_current"]
                max_pwr_list = np.full(len(self._energy_usage) + 1,max_pwr)
                self._devices[device_id]["ax"].plot(timestamps, max_pwr_list)
        else:
            ax = self._axs
            device_id = list(self._devices.keys())[0]
            ax.set_xlabel("Time (cycles)")
            ax.set_ylabel("Energy Usage (J)")
            ax.set_title(f"Device {device_id} Energy Consumption Over Time")
            self._devices[device_id]["ax"] = ax
            self._axs = ax
            # Print power limit line
            timestamps = []
            for event in self._energy_usage:
                timestamps.append(event["timestamp"])
                lastDuration = event["duration"]
            timestamps.append(timestamps[-1] + lastDuration)
            max_pwr = self._devices[device_id]["supply"]["supply_voltage"]*self._devices[device_id]["supply"]["max_supply_current"]
            max_pwr_list = np.full(len(self._energy_usage) + 1,max_pwr)
            self._devices[device_id]["ax"].plot(timestamps, max_pwr_list)

        plt.get_current_fig_manager().set_window_title(self._model_name)

        # For each device, plot event hardware energy usage onto the timeline.
        for event in self._energy_usage:
            timestamp = event["timestamp"]
            duration = event["duration"]
            for device_id, device in event["devices"].items():
                device_info = self._devices[device_id]
                y = 0
                for consumer, status, energy_usage in device:
                    c = ColorHash(consumer).rgb
                    device_info["ax"].bar(
                        [timestamp + duration / 2],
                        [energy_usage],
                        bottom=y,
                        width=duration,
                        label=f"{consumer}",
                        color=(c[0] / 255, c[1] / 255, c[2] / 255),
                    )
                    device_info["ax"].text(
                        x=timestamp + duration / 2,
                        y=y + energy_usage / 2,
                        s=f"{consumer}",
                        ha="center",
                        va="top",
                        color="black",
                    )
                    y += energy_usage

        return self._energy_usage

    def get_energy_usage_step(self, step) -> (bool, dict):
        if step < 0 or step >= len(self._energy_usage):
            return (False, {})
        else:
            return (True, self._energy_usage[step])

    def print_energy_usage(self) -> None:
        for event in self._energy_usage:
            print(f"TIME: {event['timestamp']}")
            print(event["duration"])
            for device_id, device in event["devices"].items():
                print(f"Device {device_id} energy usage:")
                sum = 0
                for consumer, status, energy_usage in device:
                    print(f"\t{consumer} ({status}) used {energy_usage} J")
                    sum += energy_usage

                print(f"\tSum: {sum}")
                print(f"\tAvailable energy: {0}")
            print()

    def visualize_energy_usage(self) -> None:
        plt.tight_layout()
        plt.show()

    def save_outputs(self):
        plt.tight_layout()
        plt.savefig("output_energy_usage.jpg")
        with open("output_energy_usage.json", 'w') as fp:
            json.dump(self._energy_usage, fp)

def get_energy_model(name, cwd):
    try:
        sys.path.append(cwd + "src/energy_model/")
        from energy_model_v0_0 import EnergyModel_V0_0
    except ImportError:
        raise Exception("Unable to load models.")

    match name:
        case "EnergyModel_V0_0":
            return EnergyModel_V0_0()
        case _:
            raise Exception("No energy model specified.")