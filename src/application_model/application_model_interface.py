"""_summary_
@file       application_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device applications.
@version    0.0.0
@date       2022-11-23
"""

from datetime import date

import matplotlib.pyplot as plt
import numpy as np
from colorhash import ColorHash


class ApplicationModelInterface:
    def __init__(self) -> None:
        self._devices = {}
        self._event_timeline = []
        self._fig, self._ax = plt.subplots()
        self._ax.set_xlabel("Time (cycles)")
        self._ax.set_ylabel("CPU")

    def add_device(self, device_name, device) -> bool:
        if device_name in self._devices:
            return False
        self._devices[device_name] = device
        return True

    def get_devices(self) -> dict:
        return self._devices

    def generate_event_timeline(self) -> dict:
        # Generate y components.
        cores = []
        for device_id, device in self._devices.items():
            for core_id, core in device["cores"].items():
                cores.append((f"{device_id}_{core_id}", device_id, core_id))

        self._ax.set_ylim(0, len(cores) * 10)
        self._ax.set_yticks([i * 10 + 5 for i in range(len(cores))])
        self._ax.set_yticklabels([label for label, _, _ in cores])

        # Plot events onto the timeline.
        for event in self._event_timeline:
            timestamp = int(event["timestamp"])
            for device_id, device in event["devices"].items():
                for core_id, core in device["cores"].items():
                    idx = 0
                    for idx_, core_ in enumerate(cores):
                        if device_id == core_[1] and core_id == core_[2]:
                            idx = idx_
                    c = ColorHash(core).rgb
                    self._ax.broken_barh(
                        [(timestamp, 1)],
                        (idx * 10 + 2, 6),
                        color=(c[0] / 255, c[1] / 255, c[2] / 255),
                    )
                    self._ax.text(
                        x=timestamp + 0.5,
                        y=idx * 10 + 9,
                        s=core,
                        ha="center",
                        va="center",
                        color="black",
                    )

        return self._event_timeline

    def get_event_timeline_step(self, step) -> (bool, dict):
        # Return event timeline step
        if step < 0 or step >= len(self._event_timeline):
            return (False, {})
        else:
            return (True, self._event_timeline[step])

    def print_event_timeline(self) -> None:
        for event in self._event_timeline:
            print(f"TIME: {event['timestamp']}")
            print(f"Outputs generated: {event['cache']}")
            print(f"Device usage:")
            for device in event["devices"].items():
                print(f"\t{device}")
            print()

    def visualize_event_timeline(self) -> None:
        plt.tight_layout()
        plt.show()
