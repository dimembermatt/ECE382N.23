"""_summary_
@file       energy_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device energy usage.
@version    0.0.0
@date       2022-11-22
"""

import sys

import matplotlib.pyplot as plt
from colorhash import ColorHash


class EnergyModelInterface:
    def __init__(self) -> None:
        self._devices = {}
        self._energy_supplies = {}
        self._energy_usage = []
        self._fig, self._ax = None, None

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
        for ax, device_id in zip(self._axs, self._devices.keys()):
            ax.set_xlabel("Time (cycles)")
            ax.set_ylabel("Energy Usage (J)")
            ax.set_title(f"Device {device_id} Energy Consumption Over Time")
            self._devices[device_id]["ax"] = ax

        # For each device, plot event hardware energy usage onto the timeline.
        for event in self._energy_usage:
            timestamp = int(event["timestamp"])
            for device_id, device in event["devices"].items():
                device_info = self._devices[device_id]
                y = 0
                for consumer, status, energy_usage in device:
                    c = ColorHash(consumer).rgb
                    device_info["ax"].bar(
                        [timestamp],
                        [energy_usage],
                        bottom=y,
                        width=1,
                        label=f"{consumer}",
                        color=(c[0] / 255, c[1] / 255, c[2] / 255),
                    )
                    device_info["ax"].text(
                        x=timestamp,
                        y=y + energy_usage,
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
