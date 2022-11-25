"""_summary_
@file       application_model_interface.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Provides the abstraction interface for modeling device applications.
@version    0.0.0
@date       2022-11-23
"""

class ApplicationModelInterface:
    def __init__(self) -> None:
        self._devices = {}
        self._event_timeline = []

    def add_device(self, device_name, device) -> bool:
        if device_name in self._devices:
            return False
        self._devices[device_name] = device
        return True

    def get_devices(self) -> dict:
        return self._devices

    def generate_event_timeline(self) -> dict:
        # Return event timeline
        # TODO: implemented by concrete class
        return self._event_timeline

    def get_event_timeline_step(self, step) -> (bool, dict):
        # Return event timeline step
        if step < 0 or step >= len(self._event_timeline):
            return (False, {})
        else:
            return (True, self._event_timeline[step])
