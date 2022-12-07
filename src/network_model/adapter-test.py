from adapter import Adapter

input = [
    {
        "timestamp": 0,
        "devices": {
            "device_0": {"cores": {"core_0": "dev_0_core_0_task_0"}, "hw": ["adc_0"]},
            "device_1": {"cores": {}, "hw": []},
        },
        "cache": [{"output_0": ["device_0"]}],
    },
    {
        "timestamp": 1,
        "devices": {
            "device_0": {"cores": {"core_0": "dev_0_core_0_task_1"}, "hw": ["comm_0"]},
            "device_1": {"cores": {}, "hw": []},
        },
        "cache": [{"output_1": ["device_1"]}],
    },
    {
        "timestamp": 2,
        "devices": {
            "device_0": {"cores": {}, "hw": []},
            "device_1": {"cores": {"core_0": "dev_1_core_0_task_2"}, "hw": ["comm_0"]},
        },
        "cache": [{"output_2": ["device_1"]}],
    },
]

device_0 = {
    "device_name": "device_0",
    "cores": {
        "core_0": {
            "active_power": 100,  # Joules
            "idle_power": 10,  # Joules
        }
    },
    "peripherals": {
        "comm_0": {
            "active_power": 20,  # Joules
            "idle_power": 10,  # Joules
        },
        "adc_0": {
            "active_power": 10,  # Joules
            "idle_power": 1,  # Joules
        },
    },
    "schedule": {
        "core_0": [
            {
                "task_name": "dev_0_core_0_task_0",
                "dependencies": [],
                "outputs": {
                    "output_0": ["device_0"],
                },
                "hw": [
                    "adc_0",
                ],
            },
            {
                "task_name": "dev_0_core_0_task_1",
                "dependencies": ["output_0"],
                "outputs": {
                    "output_1": ["device_1"],
                },
                "hw": [
                    "comm_0",
                ],
            },
        ]
    },
    "cache": [],
}

device_1 = {
    "device_name": "device_1",
    "cores": {
        "core_0": {
            "active_power": 100,
            "idle_power": 10,
        },
    },
    "peripherals": {
        "comm_0": {
            "active_power": 20,  # Joules
            "idle_power": 10,  # Joules
        },
        "adc_0": {
            "active_power": 10,  # Joules
            "idle_power": 1,  # Joules
        },
    },
    "schedule": {
        "core_0": [
            {
                "task_name": "dev_1_core_0_task_2",
                "dependencies": ["output_1"],
                "outputs": {
                    "output_2": ["device_1"],
                },
                "hw": [
                    "comm_0",
                ],
            },
        ],
        "core_1": [
            {
                "task_name": "dev_1_core_1_task_3",
                "dependencies": ["output_2"],
                "outputs": {
                    "output_3": ["device_1"],
                },
                "hw": [],
            },
            {
                "task_name": "dev_1_core_1_task_4",
                "dependencies": ["output_3"],
                "outputs": {
                    "output_4": ["device_1"],
                },
                "hw": [],
            },
            {
                "task_name": "dev_1_core_1_task_5",
                "dependencies": [],
                "outputs": {
                    "output_5": ["device_1"],
                },
                "hw": [],
            },
        ],
    },
    "cache": [],
}

device_list = [device_0, device_1]
adapter = Adapter(device_list)
adapter.create_gif(input, "test.gif")
