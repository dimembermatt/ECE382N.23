"""_summary_
@file       test_app_layer.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for testing the application layer of the model.
@version    0.0.0
@data       2022-10-13
TODO: determine whether to use pytest or doctest or w.e. for testing framework.
"""

import sys

sys.path.append("../src")

import src.application_layer.application_layer

if __name__ == "__main__":
    if sys.version[0] < 3:
        raise Exception("This program only supports Python 3.")

    # Create an application layer with a single device with a single process.
    # The process runs indefinitely, looping around two tasks.
    app_layer = ApplicationLayer()
    app_device = ApplicationDevice()
    app_process = ApplicationProcess()

    task_inputs = []  # No inputs.
    task_duration = 3  # The task runs for 3 time steps.
    task_outputs = {}  # No outputs.
    app_task = ApplicationTask(task_inputs, task_duration, task_outputs)

    app_process.add_task(app_task)
    app_process.add_loop()

    app_device.add_process(app_process)

    app_layer.add_device(app_device)

    # Begin execution.
    timeline = []
    timeline.append(app_layer.start())
    while True:
        res = app_layer.step()
        if res is None:
            break
        timeline.append(res)

    # Format timeline output. This should look like a callgraph of where
    # processes begin, which tasks are being run, when do they end, what
    # inputs/outputs are generated, etc.
    print(timeline)
