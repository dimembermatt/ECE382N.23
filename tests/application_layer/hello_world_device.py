"""_summary_
@file       hello_world_device.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models a hello world device that blinks an LED.
@version    0.0.0
@data       2022-10-13
"""

from application_layer.application_core import ApplicationCore
from application_layer.application_device import ApplicationDevice
from application_layer.application_process import ApplicationProcess
from application_layer.application_task import ApplicationTask


class HelloWorldDevice(ApplicationDevice):
    """_summary_"""

    def __init__(self, device_id=0):
        super().__init__(
            device_id=device_id,
            resources={
                "cores": [ApplicationCore(core_id=0), ApplicationCore(core_id=1)],
                "led_state": [False],
                "token": [0],
                "iteration": [0],
            }
        )

        # Pin the Hello world process to the device core.
        self.add_process(self.COMProcess())
        self.add_process(self.LEDProcess())

        # Now we wait for the device scheduler to start.

    class COMProcess(ApplicationProcess):
        """_summary_
        The COM process sends a message to the world every 10 cycles. Given the
        frequency of 1Hz, this is a period of 10 seconds. After 3 executions,
        the process finishes.
        """

        def __init__(self):
            super().__init__(process_name="COM_PROCESS")

            # Add our initial com task.
            for i in range(3):
                self.add_task(self.COMTask(i))

        class COMTask(ApplicationTask):
            """_summary_
            The COM Task generates a message every iteration.
            """

            def __init__(self, num):
                super().__init__(
                    inputs={"iteration": 1},
                    duration=10,
                    outputs=["iteration", "message"],
                    task_name=f"COM_TASK_{num}",
                )

            def execution(self):
                iteration = self.resources["iteration"].pop(0)
                self.outputs["message"].append(
                    f"HELLO WORLD I AM {self.get_task_name()}"
                )
                self.outputs["iteration"].append(iteration + 1)

    class LEDProcess(ApplicationProcess):
        """_summary_
        The hello world process consists of two tasks in the following order:
        - a task that turns on an LED
        - a task that turns off an LED
        The LED duty cycle is 50% and takes 1 cycle to execute. Given the
        core frequency of 1Hz, this is a period of 1 second.
        """

        def __init__(self):
            super().__init__(process_name="LED_PROCESS")

            # Add the two tasks to the process.
            self.add_task(self.HeartbeatOnTask())
            self.add_task(self.HeartbeatOffTask())

            # Loop them together to run indefinitely.
            self.add_loop()

        class HeartbeatOnTask(ApplicationTask):
            """_summary_
            The heartbeat on task turns on a heartbeat LED.
            """

            def __init__(self):
                super().__init__(
                    inputs={"token": 1},
                    duration=1,
                    outputs=["led_state", "token"],
                    task_name="LED_ON_TASK",
                )

            def execution(self):
                token = self.resources["token"].pop(0)
                self.outputs["led_state"].append(True)
                self.outputs["token"].append(token + 1)

        class HeartbeatOffTask(ApplicationTask):
            """_summary_
            The heartbeat off task turns off a heartbeat LED.
            """

            def __init__(self):
                super().__init__(
                    inputs={"token": 1},
                    duration=1,
                    outputs=["led_state", "token"],
                    task_name="LED_OFF_TASK",
                )

            def execution(self):
                token = self.resources["token"].pop(0)
                self.outputs["led_state"].append(False)
                self.outputs["token"].append(token + 1)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
