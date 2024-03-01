from perso_functions import update_from_yaml
import pybamm

class Battery:
    def __init__(self, config_file=None, **kwargs):
        self.capacity = 12  # in Watt-hours
        self.chemistry = 'Li - ion'  # e.g., "Lithium-ion"
        self.charging_efficiency = 0.95
        self.discharging_efficiency = 0.95
        self.thermal_management_efficiency = 0.9

        if config_file:
                update_from_yaml(self, config_file, 'battery')
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    @property
    def get_capacity(self):
        return self.capacity

    @property
    def get_chemistry(self):
        return self.chemistry

    @property
    def get_charging_efficiency(self):
        return self.charging_efficiency

    @property
    def get_discharging_efficiency(self):
        return self.discharging_efficiency

    @property
    def get_thermal_management_efficiency(self):
        return self.thermal_management_efficiency

    @property
    def set_capacity(self, capacity):
        self.capacity = capacity

    @property
    def set_chemistry(self, chemistry):
        self.chemistry = chemistry

    @property
    def set_charging_efficiency(self, charging_efficiency):
        self.charging_efficiency = charging_efficiency

    @property
    def set_discharging_efficiency(self, discharging_efficiency):
        self.discharging_efficiency = discharging_efficiency

    @property
    def set_thermal_management_efficiency(self, thermal_management_efficiency):
        self.thermal_management_efficiency = thermal_management_efficiency

    def get_battery(self, time):
        #options = {"thermal": "x-full"}
        model = pybamm.lithium_ion.DFN()
        sim = pybamm.Simulation(model)
        sim.solve([0, time])
        sim.plot(
            ["Cell temperature [K]", "Total heating [W.m-3]", "Current [A]", "Voltage [V]"]
        )

# # Example Usage
# battery_params = Battery(
#     capacity=266000,  # example capacity in Watt-hours
#     chemistry="Lithium-ion",
#     charging_efficiency=0.95,
#     discharging_efficiency=0.95,
#     thermal_management_efficiency=0.90,
# )

# # Accessing battery parameters
# print("Battery Capacity:", battery_params.get_capacity(), "Wh")
# print("Battery Chemistry:", battery_params.get_chemistry())
# print("Charging Efficiency:", battery_params.get_charging_efficiency())
# print("Discharging Efficiency:", battery_params.get_discharging_efficiency())
# print("Thermal Management Efficiency:", battery_params.get_thermal_management_efficiency())

# # Modifying battery parameters
# battery_params.set_capacity(120000)  # update capacity
# battery_params.set_thermal_management_efficiency(0.92)  # update thermal management efficiency