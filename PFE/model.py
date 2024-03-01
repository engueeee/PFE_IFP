import math
import numpy as np 
from perso_functions import update_from_yaml
from fuel_cell import FuelCell
from battery import Battery
import pymotor

class ElectricTruckModel(FuelCell,Battery):
    def __init__(self, config_file=None, **kwargs):
        # Default values
        self.mass = 19
        self.pmax = 370 #kW
        self.air_density = 1.225  # in kg/m^3 (standard atmospheric conditions)
        self.scx = 8
        self.SF = 2
        self.rolling_resistance = 0.01
        self.frein = 0
        self.motor_efficiency = 0.9
        self.transmission_efficiency = 0.95
        self.charge_efficiency = 0.95
        self.discharge_efficiency = 0.95
        self.ambient_temperature = 298.15
        self.motor_cooling_efficiency = 0.85
        self.battery_cooling_efficiency = 0.90
        self.charger_efficiency = 0.92
        self.inverter_efficiency = 0.95
        self.energy_aux = 5

        if config_file:
            update_from_yaml(self, config_file, 'all')
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def calculate_aerodynamic_drag(self, velocity): 
        return 0.5 * self.rho_air * self.scx * velocity

    def calculate_climbing_res(self, slope):
        return self.mass * 9.81 * math.sin(math.atan(slope/100))
    
    def calculate_intern_friction(self, velocity):
        a = 0.2
        return self.mass * a * velocity

    def calculate_rolling_resistance(self, slope):
        return self.rolling_resistance * self.mass * 9.81 * math.cos(math.atan(slope/100))

    def calculate_power_required(self, velocity, slope):
        drag = self.calculate_aerodynamic_drag(velocity)
        clim = self.calculate_climbing_res(slope)
        rolling_resistance = self.calculate_rolling_resistance(slope)
        intern_friction = self.calculate_intern_friction(velocity)

        total_power = (drag + rolling_resistance + clim + intern_friction) * velocity
        return total_power

    def calculate_distance_traveled(self, time, velocity):
        return velocity * time

    def calculate_motor_power(self, velocity, slope):
        energy_required = self.calculate_power_required(velocity, slope)
        motor_power = energy_required / (self.motor_efficiency * self.transmission_efficiency)
        return motor_power
    
    def calculate_wheel_energy(self, velocity, autonomie, slope):
        power_wheel = self.calculate_power_required(velocity, slope)
        return power_wheel * autonomie / (velocity * self.transmission_efficiency * self.motor_efficiency * self.charge_efficiency)
    
    def calculate_battery_energy_consumption(self, autonomie, velocity, slope):
        energy_wheel = self.calculate_wheel_energy(velocity, autonomie, slope)
        energy_consumption = (energy_wheel+self.energy_aux) / self.discharge_efficiency
        return energy_consumption
    
    def calculate_acceleration(self, delta_t, velocity):
        #acceleration = motor_power / (self.mass * velocity)  # Assuming constant acceleration
        return np.gradient(velocity, delta_t)

    def calculate_thermal_losses(self, time, velocity, slope):
        distance = self.calculate_distance_traveled(time, velocity)
        motor_power = self.calculate_motor_power(velocity, slope)
        battery_energy_consumption = motor_power * distance / self.transmission_efficiency
        motor_heat_loss = motor_power * (1 - self.motor_cooling_efficiency)
        battery_heat_loss = battery_energy_consumption * (1 - self.battery_cooling_efficiency)
        total_heat_loss = motor_heat_loss + battery_heat_loss
        return total_heat_loss

    def calculate_total_energy_consumption(self, time, velocity, slope):
        battery_energy_consumption = self.calculate_battery_energy_consumption(time, velocity, slope)
        thermal_losses = self.calculate_thermal_losses(time, velocity, slope)
        total_energy_consumption = (
            battery_energy_consumption / self.charge_efficiency
            + thermal_losses / self.inverter_efficiency
        )
        return total_energy_consumption

    def get_vmax(self):
        return 3.6 * math.pow((2 * self.pmax) / self.air_density * self.scx, 1/3)
    
    def get_mass_rot(self):
        mass_inertie = 0.03 * self.mass # Les protocoles de mesures WLTP et EPA lui donnent une équivalence à 3% de la masse du véhicule
        return mass_inertie

