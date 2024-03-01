import numpy as np 
import fuel_cell

DATA = "inputs_param.yaml"
ecomp = fuel_cell.eCompressor(config_file=DATA)

print(f'Gamma:\t{ecomp.gamma}')
print(f'T2:\t{ecomp.T2}')
print(f'w_spec:\t{ecomp.w_spec}')
print(f'Air density:\t{ecomp.rho_air}')
print(f'Air humide:\t{ecomp.rho_air_hum}')
print('Power eCompressor: %3f W'%(ecomp.comp_power))