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

print(input)
