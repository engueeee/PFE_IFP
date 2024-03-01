import pybamm
import pandas as pd

# options = {"thermal": "x-full"}
options = {"thermal": "lumped"}

model = pybamm.lithium_ion.DFN(options=options)
# models = [
#     pybamm.lithium_ion.SPM(),
#     pybamm.lithium_ion.SPMe(),
#     pybamm.lithium_ion.DFN(),
#     pybamm.lithium_ion.BasicDFN()
# ]

# sims = []
# for model in models:
#     sim = pybamm.Simulation(model)
#     sim.solve([0, 3600])
#     sims.append(sim)

parameter_values = pybamm.ParameterValues("Chen2020")
# parameter_values = pybamm.ParameterValues("Marquis2019")
# parameter_values = pybamm.ParameterValues("Mohtat2020")
# parameter_values = pybamm.ParameterValues("Ai2020")
# parameter_values = model.default_parameter_values

# parameter_values["Current function [A]"] = 3
parameter_values["Number of cells connected in series to make a battery"] = 100
# # print(parameter_values)
parameter_values["Number of electrodes connected in parallel to make a cell"] = 5

drive_cycle = pd.read_csv(
    "UDDS.csv", comment="#", header=None
).to_numpy()

# Create interpolant
current_interpolant = pybamm.Interpolant(drive_cycle[:, 0], drive_cycle[:, 1], pybamm.t)

# Set drive cycle
parameter_values["Current function [A]"] = current_interpolant

# pybamm.dynamic_plot(sims, time_unit="seconds")

# parameter_values["Current function [A]"] = 3
# parameter_values["Open-circuit voltage at 100% SOC [V]"] = 3.4
# parameter_values["Open-circuit voltage at 0% SOC [V]"] = 3.0

sim = pybamm.Simulation(model, parameter_values=parameter_values)
sim.solve()

# sim.plot(
#     ['Total current density [A.m-2]', 'Throughput capacity [A.h]',
#      'Cell temperature [C]', 'Current [A]', 'C-rate',
#      'Voltage [V]', 'Power [W]', 'Current variable [A]'
#     ]
# )
# sim.plot()
sim.plot(
    ["Cell temperature [K]", "Total heating [W.m-3]", "Current [A]", "Voltage [V]", "Volume-averaged cell temperature [K]"]
)

# Import drive cycle from file
# # model = pybamm.lithium_ion.SPMe()

# sim = pybamm.Simulation(model, parameter_values=parameter_values)
# sim.solve()

# # # parameter_values.search("currunt")
# sim.plot(["Currunt [A]", "Voltage [V]"])