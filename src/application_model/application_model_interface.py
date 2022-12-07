"""_summary_
@file       application_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device applications.
@version    0.0.0
@date       2022-11-28
"""


import json
import sys

import matplotlib.pyplot as plt
from colorhash import ColorHash


class ApplicationModelInterface:
    def __init__(self, model_name) -> None:
        self._devices = {}
        self._event_timeline = []
        self._fig, self._ax = plt.subplots()
        self._fig.suptitle("Event Timeline")
        self._ax.set_xlabel("Time (cycle)")
        self._ax.set_ylabel("CPU")
        plt.get_current_fig_manager().set_window_title(model_name)

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
            device["core_utilization"] = {}
            for core_id in device["schedule"].keys():
                device["core_utilization"][core_id] = [0, 0]
                cores.append((f"{device_id}_{core_id}", device_id, core_id))
        cores.reverse()
        self._ax.set_ylim(0, len(cores) * 10)
        self._ax.set_yticks([i * 10 + 5 for i in range(len(cores))])
        self._ax.set_yticklabels([label for label, _, _ in cores])

        # Plot events onto the timeline.
        for event in self._event_timeline:
            timestamp = event["timestamp"]
            duration = event["duration"]
            for device_id, device in self._devices.items():
                for core_id in device["cores"].keys():
                    if (
                        device_id in event["devices"]
                        and core_id in event["devices"][device_id]["cores"]
                    ):
                        task_name = event["devices"][device_id]["cores"][core_id]
                        idx = 0
                        for idx_, core_ in enumerate(cores):
                            if device_id == core_[1] and core_id == core_[2]:
                                idx = idx_
                        c = ColorHash(task_name).rgb
                        self._ax.broken_barh(
                            [(timestamp, duration)],
                            (idx * 10 + 2, 6),
                            color=(c[0] / 255, c[1] / 255, c[2] / 255),
                        )
                        self._ax.text(
                            x=timestamp + (duration / 2),
                            y=idx * 10 + 9,
                            s=task_name,
                            ha="center",
                            va="center",
                            color="black",
                        )
                        self._devices[device_id]["core_utilization"][core_id][0] += 1
                    self._devices[device_id]["core_utilization"][core_id][1] += 1

        return self._event_timeline

    def get_event_timeline_step(self, step) -> (bool, dict):
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

        print(f"CPU_UTILIZATION:")
        for device_id, device in self._devices.items():
            for core_id, core_utilization in device["core_utilization"].items():
                print(
                    f"{device_id}_{core_id}: {core_utilization[0] / core_utilization[1]}"
                )

    def visualize_event_timeline(self) -> None:
        plt.tight_layout()
        plt.show()

    def save_outputs(self):
        plt.tight_layout()
        plt.savefig("output_event_timeline.jpg")
        with open("output_event_timeline.json", "w") as fp:
            json.dump(self._event_timeline, fp)


def get_application_model(name, cwd):
    try:
        sys.path.append(cwd + "src/application_model/")
        from application_model_v0_0 import ApplicationModel_V0_0
        from application_model_v0_1 import ApplicationModel_V0_1
    except ImportError:
        raise Exception("Unable to load models.")

    match name:
        case "ApplicationModel_V0_0":
            return ApplicationModel_V0_0()
        case "ApplicationModel_V0_1":
            return ApplicationModel_V0_1()
        case _:
            raise Exception("No application model specified.")
