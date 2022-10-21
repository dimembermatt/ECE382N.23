"""_summary_
@file       test_app_layer_hello_world.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests a custom device, HelloWorldDevice with its own unique processes.
@version    0.0.0
@data       2022-10-16
"""

import sys

sys.path.append("../../src")
sys.path.append("../src")

from application_layer.application_layer import ApplicationLayer
from hello_world_device import HelloWorldDevice


def test_hello_world():
    """_summary_
    Create a model for a network consisting of a single HelloWorldDevice, The
    device has two cores, and runs two processes and three tasks.
    """
    app_layer = ApplicationLayer()
    hello_world_device = HelloWorldDevice(device_id=0)
    app_layer.add_device(hello_world_device)

    # Assert that the device ID is 0.
    assert hello_world_device.get_device_id() == 0

    # Assert that there is only one device on the network.
    assert len(app_layer.get_devices()) == 1

    # Assert that there are two cores.
    assert len(hello_world_device.get_resources()["cores"]) == 2

    # Assert that there are two processes yet to be scheduled.
    assert len(hello_world_device.get_processes()) == 2

    # Schedule the first batch of processes.
    app_layer.initialize_layer()

    # Assert the following:
    # - There is only one timeline entry.
    # - This entry is at the start of time, time being 0ms.
    # - In this entry, there is only one device. It contains two cores, of core
    #   IDs 0 and 1.
    # - Each core is assigned one process, COM_PROCESS and LED_PROCESS
    #   respectively.
    # - The current task for each process is COM_TASK_0 and LED_ON_TASK.
    # - There are three initial available resources: an led_state, a token, and
    #   an iteration. There is only one entry for each resource.
    event_timeline = app_layer.get_event_timeline()
    print(event_timeline[0])
    assert len(event_timeline) == 1
    assert event_timeline[0][0] == 0
    assert len(event_timeline[0][1]) == 2
    assert event_timeline[0][1][0][0] == "dev_0"
    assert event_timeline[0][1][0][1] == "core_0"
    assert event_timeline[0][1][0][2] == "LED_PROCESS"
    assert event_timeline[0][1][0][3] == "LED_ON_TASK"
    assert event_timeline[0][1][0][4] == 1000
    assert event_timeline[0][1][1][0] == "dev_0"
    assert event_timeline[0][1][1][1] == "core_1"
    assert event_timeline[0][1][1][2] == "COM_PROCESS"
    assert event_timeline[0][1][1][3] == "COM_TASK_0"
    assert event_timeline[0][1][1][4] == 10000

    resources = hello_world_device.get_resources()
    assert len(resources["led_state"]) == 1
    assert len(resources["token"]) == 1
    assert len(resources["iteration"]) == 1
    assert resources["led_state"][-1] == False
    assert resources["token"][0] == 0
    assert resources["iteration"][0] == 0

    # Run for 1 step.
    app_layer.step_layer()

    # Assert the following:
    # - Two timeline entries,
    # - Time is now 1000ms, LED_ON_TASK is completed and LED_OFF_TASK has now
    #   begun.
    # - led_state has an added entry, True, and the token is now 1 as generated
    #   by the LED_ON_TASK outputs. The iteration token was consumed by the
    #   COM_TASK_0 and is empty.
    event_timeline = app_layer.get_event_timeline()
    assert len(event_timeline) == 2
    assert event_timeline[1][0] == 1000
    assert event_timeline[1][1][0][3] == "LED_OFF_TASK"
    assert event_timeline[1][1][1][3] == "COM_TASK_0"

    resources = hello_world_device.get_resources()
    assert len(resources["led_state"]) == 2
    assert len(resources["token"]) == 1
    assert len(resources["iteration"]) == 0
    assert resources["led_state"][-1] == True
    assert resources["token"][0] == 1

    # Run for another 9 steps.
    for i in range(9):
        app_layer.step_layer()
        event_timeline = app_layer.get_event_timeline()

    # Assert the following:
    # - Eleven timeline entries,
    # - Time is now 10000ms, Currently LED_ON_TASK and COM_TASK_1.
    # - led_state's latest entry is False, and the token is now 10. The
    #   iteration token is generated and reconsumed.
    event_timeline = app_layer.get_event_timeline()
    assert len(event_timeline) == 11
    assert event_timeline[10][0] == 10000
    assert event_timeline[10][1][0][3] == "LED_ON_TASK"
    assert event_timeline[10][1][1][3] == "COM_TASK_1"

    resources = hello_world_device.get_resources()
    assert len(resources["led_state"]) == 11
    assert len(resources["token"]) == 1
    assert len(resources["iteration"]) == 1
    assert resources["led_state"][-1] == False
    assert resources["token"][0] == 10

    # Run for another 20 steps.
    for i in range(20):
        app_layer.step_layer()

    # By this point, core 1 should not have any processes scheduled, since
    # COM_TASK_3 has completed and does not loop.
    # We should also have three messages waiting to be sent to the network
    # layer.
    event_timeline = app_layer.get_event_timeline()
    assert len(event_timeline) == 31
    assert event_timeline[30][0] == 30000
    assert event_timeline[30][1][0][3] == "LED_ON_TASK"
    assert event_timeline[30][1][1][3] == "NONE"

    resources = hello_world_device.get_resources()
    assert len(resources["led_state"]) == 31
    assert len(resources["message"]) == 3
    assert resources["message"][2] == "HELLO WORLD I AM COM_TASK_2"


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    test_hello_world()
