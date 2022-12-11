"""_summary_
@file       application_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device applications.
@version    0.0.0
@date       2022-12-11
"""


import json
import sys

import matplotlib.pyplot as plt
from colorhash import ColorHash

from application_model.execution_model.application_execution_model_v0_0 import \
    ApplicationExecutionModel_V0_0
from application_model.execution_model.application_execution_model_v0_1 import \
    ApplicationExecutionModel_V0_1
from application_model.hardware_model.application_hardware_model_v0_0 import \
    ApplicationHardwareModel_V0_0
from application_model.timing_model.application_timing_model_v0_0 import \
    ApplicationTimingModel_V0_0
from application_model.timing_model.application_timing_model_v0_1 import \
    ApplicationTimingModel_V0_1
from application_model.timing_model.application_timing_model_v0_2 import \
    ApplicationTimingModel_V0_2
from application_model.timing_model.application_timing_model_v0_3 import \
    ApplicationTimingModel_V0_3


def get_app_hardware_models(hardware_model_str):
    match hardware_model_str:
        case "ApplicationHardwareModel_V0_0":
            # Hardware usage is either active or idle for the duration of the
            # task.
            return ApplicationHardwareModel_V0_0()
        case _:
            return None


def get_app_execution_models(execution_model_str):
    match execution_model_str:
        case "ApplicationExecutionModel_V0_0":
            # Execution consumes arbitrary dependencies and generate
            # arbitrary outputs without considering actual values.
            return ApplicationExecutionModel_V0_0()
        case "ApplicationExecutionModel_V0_1":
            # Execution consumes and generates real values which are
            # processed by a user defined function.
            return ApplicationExecutionModel_V0_1()
        case _:
            return None


def get_timing_models(timing_model_str):
    match timing_model_str:
        case "ApplicationTimingModel_V0_0":
            # Timing is logical and each task is considered a single cycle.
            return ApplicationTimingModel_V0_0()
        case "ApplicationTimingModel_V0_1":
            # Timing is provided by a task duration in cycles.
            return ApplicationTimingModel_V0_1()
        case "ApplicationTimingModel_V0_2":
            # Timing is dictated by a task duration in cycles and processor
            # in hertz.
            return ApplicationTimingModel_V0_2()
        case "ApplicationTimingModel_V0_3":
            # Task timing is provided a function where the duration in cycles is
            # dependent on the inputs. Afterwards the real duration is generated
            # using the processor frequency.
            return ApplicationTimingModel_V0_3()
        case "ApplicationTimingModel_V0_4":
            # TODO: ApplicationTimingModel_V0_4
            # Task timing is provided a function where the duration in cycles is
            # dependent on the inputs. Afterwards the real duration is generated
            # using the processor frequency. Likewise, the user specifies a
            # function that transforms the processor base frequency based on the
            # energy consumption of the device and the remaining supply power.
            return None
        case _:
            return None


class ApplicationModelInterface:
    def __init__(
        self, path, inputs, hardware_model_str, execution_model_str, timing_model_str
    ):
        sys.path.append(path)
        self.path = path
        self.timing_model = get_timing_models(timing_model_str)
        self.execution_model = get_app_execution_models(execution_model_str)
        self.hardware_model = get_app_hardware_models(hardware_model_str)
        self.inputs = inputs
        self.outputs = {"next_timestep": 0, "steps": {}}

        print("Running the following application submodel sub-submodels:")
        print(f"\t-Timing Model: {self.timing_model.get_model_name()}")
        print(f"\t-Execution Model: {self.execution_model.get_model_name()}")
        print(f"\t-Hardware Model: {self.hardware_model.get_model_name()}")

    def generate_output(self, num_steps=None):
        if num_steps is None:
            while True:
                can_run = self.timing_model.process_step(self.outputs, self.inputs)
                self.execution_model.process_step(self.outputs, self.inputs)
                self.hardware_model.process_step(self.outputs, self.inputs)
                if can_run is False:
                    break
        else:
            for _ in range(num_steps):
                can_run = self.timing_model.process_step(self.outputs, self.inputs)
                self.execution_model.process_step(self.outputs, self.inputs)
                self.hardware_model.process_step(self.outputs, self.inputs)
                if can_run is False:
                    break

        plt.figure(0)
        fig = plt.gcf()
        fig.set_size_inches(10, 5, forward=True)
        fig.suptitle("Application Event Timeline")
        plt.subplot(111)
        ax = plt.gca()

        # Generate y components of the event timeline corresponding to each
        # device and device processor.
        processors = []
        for device_name, device in self.inputs.items():
            for cpu_name, _ in device["hardware"].items():
                if "cpu" in cpu_name:
                    processors.append((device_name, cpu_name))

        ax.set_ylim(0, len(processors) * 10)
        ax.set_yticks([i * 10 + 5 for i in range(len(processors))])
        ax.set_yticklabels(
            [f"{device_name}_{cpu_name}" for device_name, cpu_name in processors]
        )

        for step in self.outputs["steps"].values():
            timestep = step["timestep"]
            for device_name, device in step["started_tasks"].items():
                for cpu_name, (task_name, task_duration, task_data) in device.items():
                    cpu_idx = processors.index((device_name, cpu_name))

                    c = [x / 255 for x in ColorHash(task_name).rgb]
                    ax.broken_barh(
                        [(timestep, task_duration)], (cpu_idx * 10 + 2, 6), color=[*c]
                    )
                    ax.text(
                        x=timestep + (task_duration / 2),
                        y=cpu_idx * 10 + 9,
                        s=task_name,
                        ha="center",
                        va="center",
                        color="black",
                    )

        ax.set_xlabel("Timestep (cycles)")

        return self.outputs

    def print_outputs(self):
        print(json.dumps(self.outputs, indent=4))

    def pprint_outputs(self):
        for step_idx, step in self.outputs["steps"].items():
            print(f"Step {step_idx}.")
            print(f"Timestep {step['timestep']}.")
            if len(step["started_tasks"]) > 0:
                print(f"Tasks started on this timestep:")
                for device_name, device in step["started_tasks"].items():
                    for cpu_name, (
                        task_name,
                        task_duration,
                        task_data,
                    ) in device.items():
                        print(
                            f"\t-{task_name} on {device_name}|{cpu_name}, with dependencies {task_data['dependencies']}. It will run for {task_duration} cycle(s)."
                        )
            else:
                print(f"No tasks were started on this timestep.")

            if len(step["running_tasks"]) > 0:
                print(f"Tasks also currently running on this timestep:")
                for device_name, device in step["running_tasks"].items():
                    for cpu_name, (
                        task_name,
                        task_duration,
                        task_data,
                    ) in device.items():
                        print(
                            f"\t-{task_name} on {device_name}|{cpu_name}, will run for {task_duration} more cycle(s)."
                        )
            else:
                print(f"No other tasks are currently running on this timestep.")

            if len(step["ending_tasks"]) > 0:
                print(f"Tasks finished by the end of this timestep:")
                for device_name, device in step["ending_tasks"].items():
                    for cpu_name, (
                        task_name,
                        task_duration,
                        task_data,
                    ) in device.items():
                        print(
                            f"\t-{task_name} on {device_name}|{cpu_name}, generating outputs {task_data['results']}."
                        )
            else:
                print(f"No other tasks have completed on this timestep.")

    def visualize_event_timeline(self):
        plt.show()

    def save_outputs(self):
        plt.figure(0)
        plt.tight_layout()
        fig = plt.gcf()
        fig.savefig(f"{self.path}output_event_timeline.png", dpi=100)
        with open(f"{self.path}output_event_timeline.json", "w") as fp:
            json.dump(self.outputs, fp, indent=4)
