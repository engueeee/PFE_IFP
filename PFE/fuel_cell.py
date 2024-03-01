import matplotlib.pyplot as plt
from opem.Static.Larminie_Dicks import Static_Analysis as Stat_Ana_Larminie
from opem.Static.Amphlett import Static_Analysis as Stat_Ana_Amphlett
from opem.Dynamic.Padulles_Amphlett import Dynamic_Analysis as Stat_Dyna_Amphlett
from thermo.chemical import Chemical
from perso_functions import update_from_yaml
import math

class eCompressor : 
    def __init__(self, config_file=None, **kwargs) -> None:
        self.isentropic_eff = 0.75
        self.power = 15 #kW
        self.T1 = 298.15
        self.P2C = 162650 #Pa
        self.P1C = 101325 #Pa 
        self.x_o2 = 0.21
        self.x_n2 = 0.79
        self.m_air = 80 #g/s
        self.elec_efficiency = 0.9

        if config_file:
                update_from_yaml(self, config_file, 'eCompressor')
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    @property
    def w_spec(self) -> float:
        water = Chemical('water',T=self.T1, P=self.P1C)
        p_vs = water.VaporPressure(self.T1)
        return 0.622 * p_vs / (self.P1C - p_vs)
    
    @property
    def rho_air_hum(self) -> float: 
        return (1 + self.w_spec) * self.P1C / (461.52 * (0.622 + self.w_spec) * self.T1)

    def get_capacity(self, specy) -> list:
        spec = Chemical(specy,T=self.T1, P=self.P1C)
        return spec.Cpg, spec.Cvg
    
    def get_air_capa(self, water=bool) -> list:
        o2 = Chemical('oxygen',T=self.T1, P=self.P1C)
        n2 = Chemical('Nitrogen',T=self.T1, P=self.P1C)
        if water == True:
            cp_wat, cv_wat = self.get_capacity('water')
            cp_air = (self.x_n2 * n2.Cpg + self.x_o2 * o2.Cpg) * (1-self.w_spec) + self.w_spec * cp_wat
            cv_air = (self.x_n2 * n2.Cvg + self.x_o2 * o2.Cvg) * (1-self.w_spec) + self.w_spec * cv_wat
            return cp_air, cv_air
        else:
            cp_air = self.x_n2 * n2.Cpg + self.x_o2 * o2.Cpg
            cv_air = self.x_n2 * n2.Cvg + self.x_o2 * o2.Cvg
            return cp_air, cv_air
    
    @property
    def gamma(self) -> float:
        cp_air, cv_air = self.get_air_capa(water=True)
        return cp_air / cv_air
    
    @property
    def T2(self) -> float: 
        T2s = self.T1 * (math.pow((self.P2C/self.P1C),(self.gamma - 1)/self.gamma))
        return (self.T1 + self.isentropic_eff * (T2s - self.T1))
    
    @property
    def rho_air(self) -> float: 
        o2 = Chemical('oxygen',T=self.T1, P=self.P1C)
        n2 = Chemical('Nitrogen',T=self.T1, P=self.P1C)
        water = Chemical('water',T=self.T1, P=self.P1C)
        # print(f'Water density G:\t{water.rhog}')
        # print(f'Water density Normal:\t{water.rho}')
        return (self.x_n2 * n2.rhog + self.x_o2 * o2.rhog) * (1-self.w_spec) + self.w_spec * water.rhog
    
    @property
    def comp_power(self) -> float:
        cp, _ = self.get_air_capa(water=False)
        return 1 / self.isentropic_eff * self.m_air * 1e-3 * cp * self.T1 * (math.pow((self.P2C/self.P1C),(self.gamma - 1)/self.gamma))
    
    @property
    def elec_power(self) -> float:
        return 1 / self.elec_efficiency * self.comp_power
    
class FuelCell (eCompressor): 
    def __init__(self, config_file=None, **kwargs) -> None:
        self.N = 370
        self.active_area = 50
        self.P02 = self.P2C * 1e-5

        if config_file:
                update_from_yaml(self, config_file, 'all')
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def get_Amphlett_dynamic(self):
        Test_Vector = {"A": self.active_area,"l": 0.0178,"lambda": 23,"JMax": 1.5,"T": self.T2,"N0": self.N,"KO2": 0.0000211,
                        "KH2": 0.0000422,"KH2O": 0.000007716,"tH2": 3.37,"tO2": 6.74,"t1": 2,"t2": 2,
                        "tH2O": 18.418,"rho": self.rho_air,"qMethanol": 0.0002,"CV": 2,"i-start": 0.1,"i-stop": 100,
                        "i-step": 0.1,"Name": "Padulles_Amphlett_Test"}
        data = Stat_Dyna_Amphlett(InputMethod=Test_Vector,TestMode=True,PrintMode=False,ReportMode=False)
        data['Name'] = 'Amphlett Dynamic'
        return data
    
    def get_Amphlett_static(self):
        Test_Vector={"T": self.T2,"PH2": 1.5,"PO2": self.P02,"i-start": 0,"i-stop": 100,"i-step": 0.1,"A": self.active_area,"l": 0.0178,"lambda": 23,
                     "N": self.N,"R": 0,"JMax": 1.5,"Name": "Amphlett_Test"}
        data = Stat_Ana_Amphlett(InputMethod=Test_Vector,TestMode=True,PrintMode=False,ReportMode=False)
        data['Name'] = 'Amphlett Static'
        return data
    
    def get_Larminie_static(self):
        Test_Vector = {"A": 0.06,"E0": 1.178,"T": self.T2,"RM": 0.0018,"i_0": 0.00654,"i_L": 100.0,"i_n": 0.23,"N": self.N,
                       "i-start": 0.1,"i-stop": 100,"i-step": 0.1,"Name": "Larminiee_Test"}
        data = Stat_Ana_Larminie(InputMethod=Test_Vector, TestMode=True, PrintMode=False, ReportMode=False)
        data['Name'] = 'Larminie Static'
        return data

    def plot_variables(self, datas, var, colors):
        fig, ax1 = plt.subplots(figsize=(8, 5))
        ax2 = ax1.twinx()

        for i, data in enumerate(datas):
            ax1.plot(data['I'], data[var], colors[i])
            ax2.plot(data['I'], data['EFF'], colors[i], linestyle='dashed')
            fig.legend(data['Name'])
       
        # Adding labels and title
        ax1.set_xlabel('Current (A)')
        ax1.set_ylabel(var)
        ax2.set_ylabel('Efficiency')
        fig.tight_layout()
        plt.grid()
        ax2.legend(loc='upper right')
        plt.show()

    def plot_variables_gpt(self, datas, x, y, y2, colors): 
        """
        datas: data list:
        P,
        I,
        Eta_Active,
        Eta_Conc,
        Eta_Ohmic (V),
        VE,
        EFF,
        V,
        Ph: Thermal Power,
        V0: Linear approx,
        K: slope linear app,
        x: data column for the abscisse axis
        y: data column for the first plot
        y2: data column for the second plot in dashed line

        """
        for i, data in enumerate(datas):
            fig, ax1 = plt.subplots(figsize=(8, 5))
            ax2 = ax1.twinx()
            x_axis = data[x]
            y_axis = data[y]
            y2_axis = data[y2]
            ax1.plot(x_axis, y_axis, colors[i])
            ax2.plot(x_axis, y2_axis, 'r', linestyle='dashed')
            # Adding labels and title
            ax1.set_xlabel('Current (A)')
            ax1.set_ylabel(y)
            ax2.set_ylabel(y2)
            fig.tight_layout()
            plt.title(data['Name'])
            plt.grid()
            plt.show()
