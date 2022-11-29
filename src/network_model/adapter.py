
from grapher import Grapher, Node

IMAGE_CACHE = "image-cache"

ACTIVE_NODE_COLOR = "#FFC0CB"
IDLE_NODE_COLOR = "#FFFFFF"

ACTIVE_EDGE_COLOR = "#FF0000"
IDLE_EDGE_COLOR = "#000000"

input = [
    {
        'timestamp': 0,
        'devices': {
            'device_0': {
                'cores': {
                    'core_0': 'dev_0_core_0_task_0'
                },
                'hw': ['adc_0']
            },
            'device_1': {
                'cores': {},
                'hw': []
            }
        },
        'cache': [
            {
                'output_0': ['device_0']
            }
        ]
    },
    {
        'timestamp': 1,
        'devices': {
            'device_0': {
                'cores': {
                    'core_0': 'dev_0_core_0_task_1'
                },
                'hw': ['comm_0']
            },
            'device_1': {
                'cores': {},
                'hw': []
            }
        },
        'cache': [
            {
                'output_1': ['device_1']
            }
        ]
    },
    {
        'timestamp': 2,
        'devices': {
            'device_0': {
                'cores': {},
                'hw': []
            },
            'device_1': {
                'cores': {
                    'core_0': 'dev_1_core_0_task_2'
                },
                'hw': ['comm_0']
            }
        },
        'cache': [
            {
                'output_2': ['device_1']
            }
        ]
    }
]

device_0 = {
    "device_name": "device_0",
    "cores": {
        "core_0": {
            "active_power": 100, # Joules
            "idle_power": 10, # Joules
        }
    },
    "peripherals": {
        "comm_0": {
            "active_power": 20, # Joules
            "idle_power": 10, # Joules
        },
        "adc_0": {
            "active_power": 10, # Joules
            "idle_power": 1, # Joules
        }
    },
    "schedule": {
        "core_0": [
            {
                "task_name": "dev_0_core_0_task_0",
                "dependencies": [],
                "outputs": {
                    "output_0": ["device_0"],
                },
                "hw": ["adc_0", ],
            },
            {
                "task_name": "dev_0_core_0_task_1",
                "dependencies": ["output_0"],
                "outputs": {
                    "output_1": ["device_1"],
                },
                "hw": ["comm_0", ],
            },
        ]
    },
    "cache": []
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
            "active_power": 20, # Joules
            "idle_power": 10, # Joules
        },
        "adc_0": {
            "active_power": 10, # Joules
            "idle_power": 1, # Joules
        }
    },
    "schedule": {
        "core_0": [
            {
                "task_name": "dev_1_core_0_task_2",
                "dependencies": ["output_1"],
                "outputs": {
                    "output_2": ["device_1"],
                },
                "hw": ["comm_0", ],
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
        ]
    },
    "cache": []
}

class TimelineEntry:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.active_device_list = []
        self.transaction_list = []

    def __str__(self):
        return f'{self.timestamp} {self.active_device_list} {self.transaction_list}'

class Adapter:

    def __init__(self, device_list):
        self.device_list = device_list

        # certain outputs map to an outside device. keep track of those here
        self.output_map = {}
        self.output_src_map = {}
        self.connected_devices = {}
        self.node_list = []

        for device in self.device_list:
            device_name = device['device_name']
            connected_device_list = []

            for core in device['schedule']:
                for task in device['schedule'][core]:
                    for output in task['outputs']:
                        self.output_src_map[output] = device_name
                        output_dst = []
                        for connected_device in task['outputs'][output]:
                            if connected_device != device_name:
                                output_dst.append(connected_device)

                                if connected_device not in self.connected_devices:
                                    connected_device_list.append(connected_device)

                        self.output_map[output] = output_dst
            self.connected_devices[device_name] = connected_device_list
            
            # create nodes for each device
            node = Node(device_name, connected_device_list)
            self.node_list.append(node)

    def create_timeline(self, input):
        timeline = []

        for entry in input:
            timeline_entry = TimelineEntry(entry['timestamp'])

            for device in entry['devices']:
                if entry['devices'][device]['cores']:
                    timeline_entry.active_device_list.append(device)
                    continue
            
            for cache in entry['cache']:
                for output in cache:
                    if output in self.output_map:
                        for connected_device in self.output_map[output]:
                            src_device = self.output_src_map[output]
                            timeline_entry.transaction_list.append((src_device, connected_device))

            timeline.append(timeline_entry)

        return timeline

    def create_gif(self, input, gif_path):
        timeline = self.create_timeline(input)
        grapher = Grapher(self.node_list)
        grapher.set_image_time(-1)
        grapher.save_graph_as_image(IMAGE_CACHE)

        for entry in timeline:
            active_device_list = entry.active_device_list
            transaction_list = entry.transaction_list

            for node in self.node_list:
                if node.node_id in active_device_list:
                    grapher.set_node_color(node.node_id, ACTIVE_NODE_COLOR)
                else:
                    grapher.set_node_color(node.node_id, IDLE_NODE_COLOR)

            for device_name in self.connected_devices:
                for connected_device in self.connected_devices[device_name]:
                    if (device_name, connected_device) in transaction_list:
                        grapher.set_edge_color(device_name, connected_device, ACTIVE_EDGE_COLOR)
                    else:
                        grapher.set_edge_color(device_name, connected_device, IDLE_EDGE_COLOR)

            grapher.set_image_time(entry.timestamp)
            grapher.save_graph_as_image(IMAGE_CACHE)
        
        grapher.generate_gif(grapher.screenshot_list, gif_path)

