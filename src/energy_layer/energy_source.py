"""_summary_
@file       energy_source.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Manages the energy production and storage of a given power
            supply/storage solution.
@version    0.0.0
@date       2022-10-21
"""


class EnergySource:
    """_summary_
    Estimates and models a power supply or storage device.
    """

    source_id = 0

    def __init__(
        self,
        source_info={
            "watt_limit": 1,
        },
    ):
        """_summary_
        An energy source has at least the following:
        - watt limit: a limit on the power consumption of the device

        Args:
            source_info (dict, optional): Power source information. Defaults to {"watt_limit": 1,}.
        """
        self.source_info = source_info
        self.power_draw = 0

        self.core_id = ApplicationCore.core_id
        ApplicationCore.core_id += 1

    def draw_power(self, power):
        """_summary_
        Draws power from the source if it does not go over the power limit.

        Args:
            power: watts to be drawn from the source

        Returns:
            Bool: True if power can be drawn without going over the limit
        """
        if self.source_info["watt_limit"] < power + self.power_draw:
            return False
        else:
            self.power_draw += power
            return True

    def return_power(self, power):
        """_summary_
        Stops drawing power from the power source.

        Args:
            power: watt capacity to be returned to the power source

        Returns:
            Bool: True if power draw can be returned without going negative
        """
        if self.power_draw < power:
            return False
        else:
            self.power_draw -= power
            return True

    def get_source_id(self):
        return self.source_id
