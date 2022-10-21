"""_summary_
@file       test_app_layer.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for testing the application layer of the model.
@version    0.0.0
@data       2022-10-16
"""

import sys

sys.path.append("../../src")
sys.path.append("../src")

from application_layer.application_core import ApplicationCore
from application_layer.application_device import ApplicationDevice
from application_layer.application_layer import ApplicationLayer
from application_layer.application_process import ApplicationProcess
from application_layer.application_task import ApplicationTask


def test_default_app():
    """_summary_
    Create a model for a network consisting of one device, which consists of a
    single CPU. There are two processes each with one task that must be
    executed.
    """
    app_layer = ApplicationLayer()
    app_device = ApplicationDevice(device_id=0, resources={"cores": [ApplicationCore(core_id=0)], "key": [0]})

    app_process = ApplicationProcess(process_name="PROC1")
    app_task = ApplicationTask(
        inputs={"key": 1}, duration=5, outputs=["key"], task_name="TASK1"
    )
    app_process.add_task(app_task)
    app_device.add_process(app_process)

    app_process2 = ApplicationProcess(process_name="PROC2")
    app_task2 = ApplicationTask(
        inputs={"key": 1}, duration=10, outputs=["key"], task_name="TASK2"
    )
    app_process2.add_task(app_task2)
    app_device.add_process(app_process2)

    app_layer.add_device(app_device)

    # Assert that the device ID is 0.
    assert app_device.get_device_id() == 0

    # Schedule the first batch of processes.
    app_layer.initialize_layer()

    # Assert the following:
    # - There is only one timeline entry.
    # - This entry is at the start of time, time being 0ms.
    # - In this entry, there is only one device. It contains a single core, with
    #   a single process and running task.
    # - This task has an execution duration of 5 cycles converted into ms. This
    #   is 5000 ms or 5 s, since the default core frequency is 1Hz.
    event_timeline = app_layer.get_event_timeline()
    assert len(event_timeline) == 1
    assert event_timeline[0][0] == 0
    assert event_timeline[0][1][0][2] == "PROC1"
    assert event_timeline[0][1][0][3] == "TASK1"
    assert event_timeline[0][1][0][4] == 5000

    # Run for 1 step.
    app_layer.step_layer()

    # Assert the following:
    # - There are now two timeline entries.
    # - The second entry is at T=5000ms.
    # - In this entry, there still is only one device. It contains a single
    #   core, with a single process and running task.
    # - The process and task are now different.
    # - This task has an execution duration of 10 cycles converted into ms. This
    #   is 10000 ms or 10 s, since the default core frequency is 1Hz.
    event_timeline = app_layer.get_event_timeline()
    assert len(event_timeline) == 2
    assert event_timeline[1][0] == 5000
    assert event_timeline[1][1][0][2] == "PROC2"
    assert event_timeline[1][1][0][3] == "TASK2"
    assert event_timeline[1][1][0][4] == 10000

    # Run for 1 step.
    app_layer.step_layer()

    # Assert the following:
    # - There are now three timeline entries.
    # - The third entry is at T=15000ms.
    # - In this entry, there still is only one device. However, it contains no
    #   processes.
    event_timeline = app_layer.get_event_timeline()
    assert len(event_timeline) == 3
    assert event_timeline[2][0] == 15000
    assert event_timeline[2][1][0][2] == "NONE"
    assert event_timeline[2][1][0][3] == "NONE"
    assert event_timeline[2][1][0][4] == 0

    # Assert that the resources of the single device on network consists of a
    # core, and a key with a value of 2. There is only one entry in the key.
    assert len(app_device.get_resources()["key"]) == 1
    assert app_device.get_resources()["key"][0] == 2


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    test_default_app()
