"""_summary_
@file       hello_world_device.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models a hello world device that blinks an LED.
@version    0.0.0
@data       2022-10-13
"""


class HelloWorldDevice(ApplicationDevice):
    """_summary_
    The hello world device has one core and one peripheral, an LED. This device
    is sourced unlimited power from the wall outlet. The relevant power details
    of each is described in the energy layer, which we don't deal with here. It
    runs one infinite process, the HelloWorldProcess. We use the default
    scheduler.
    """

    def __init__(self):
        # Give the device one starting resource: a trivial token. This token
        # a dependency consumed by the tasks in HelloWorldProcess. Each task
        # regenerates the token at the end of execution.
        super().__init__(num_cores=1, resources={"token": 0})

        # Pin the Hello world process to the device core.
        self.add_process(self.HelloWorldProcess())

        # Now we wait for the device scheduler to start.

    class HelloWorldProcess(ApplicationProcess):
        """_summary_
        The hello world process consists of two tasks in the following order:
        - a task that turns on an LED
        - a task that turns off an LED
        The LED duty cycle is 50% for a frequency of 1 Hz. (Each task runs for
        500 ms before cycling.)
        """

        def __init__(self):
            super().__init__()

            # Add the two tasks to the process.
            heartbeat_on_task = self.HeartbeatOnTask(
                {"token": []}, 500, {"led_state": None, "token": []}
            )
            heartbeat_off_task = self.HeartbeatOffTask(
                {"token": []}, 500, {"led_state": None, "token": []}
            )
            self.add_task(heartbeat_on_task)
            self.add_task(heartbeat_off_task)

            # Loop them together to run indefinitely.
            self.add_loop()

        class HeartbeatOnTask(ApplicationTask):
            """_summary_
            The heartbeat on task turns on a heartbeat LED.
            """

            def execute(self):
                """_summary_
                Consumes a token, sets the led state as True, and generates a
                token.
                """
                token = self.inputs["token"].pop(0)
                self.outputs["led_state"] = True
                self.outputs["token"].append(token + 1)

            def get_task_name(self):
                return "HEARTBEAT_ON"

        class HeartbeatOffTask(ApplicationTask):
            """_summary_
            The heartbeat off task turns off a heartbeat LED.
            """

            def execute(self):
                """_summary_
                Consumes a token, sets the led state as False, and generates a
                token.
                """
                token = self.inputs["token"].pop(0)
                self.outputs["led_state"] = False
                self.outputs["token"].append(token + 1)

            def get_task_name(self):
                return "HEARTBEAT_OFF"
