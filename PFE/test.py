import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wltp_cycle import generate_wltp_cycle
import model as model
from wltp_cycle import simulate_electric_truck_cycle
import fuel_cell as fc
import battery as batt
import pandas as pd

colors = ['b','g','r','m','c']
DATA = "inputs_param.yaml"

# time, speed = generate_wltp_cycle()
# df = pd.DataFrame()
# df['time'] = time
# df['speed'] = speed
# df['slope'] = np.zeros_like(speed)

#fuel_cell = fc.FuelCell(T=343.25,N=350,A=50)
# fuel_cell = fc.FuelCell(config_file=DATA)
battery = batt.Battery(config_file=DATA)
battery.get_battery(3600)
# data_dyna_amp = fuel_cell.get_Amphlett_dynamic()
# data_lar = fuel_cell.get_Larminie_static()
# data_amp = fuel_cell.get_Amphlett_static()
# datas = [data_amp]
# #fuel_cell.plot_variables(datas=datas,var='P',colors=colors)
# fuel_cell.plot_variables_gpt(datas=datas,x='I',y='P',y2='EFF',colors=colors)

# truck = model.ElectricTruckModel(mass=19e3,frontal_area=10,rolling_resistance=0.01,drag_coefficient=8)
# truck = model.ElectricTruckModel(config_file=DATA)
# powers = []
# for i in enumerate(np.size(speed)):
#     power = truck.calculate_total_energy_consumption(time=df['time'][i],velocity=df['speed'][i],slope=df['slope'][i])
#     powers.append(power)
# plt.plot(powers,time)


