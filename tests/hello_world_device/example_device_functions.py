"""_summary_
@file       example_device_functions.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Functions specified by the designer for modeling usage.
@version    0.0.0
@date       2022-12-10
"""

def sample_adc(argc, argv):
    # argv is empty.
    return [[1, 6, 0, 0, 10]]

def filter_adc(argc, argv):
    # argv consists of a list of adc samples.
    # [[sample, ...]]
    samples = argv[0]
    filtered_samples = []
    for sample in samples:
        if sample > 5:
            filtered_samples.append(5)
        else:
            filtered_samples.append(sample)

    return [filtered_samples]

def control_led(argc, argv):
    # argv consists of a list of filtered adc samples.
    # [[sample, ...]]
    samples = argv[0]
    if sum(samples) / len(samples) < 2.5:
        return ["LED ON"]
    return ["LED OFF"]

def sample_adc_dur(argc, argv):
    return 10

def filter_adc_dur(argc, argv):
    return 4

def control_led_dur(argc, argv):
    return 1