import sys
from io import StringIO

from .EntryVar import EntryVar
from .ResultVar import ResultVar
from .ToggleVar import ToggleVar
from .MATVar import MATVar
from .TXTVar import TXTVar
from .GasVar import GasVar
from .Section import Section
from .SimPage import SimPage
from .SimulateLiquidPage import SimulateLiquidPage

''' Create input variables for DesignLiquid and organize into Sections. '''
#Goal
max_thrust = EntryVar('max_thrust','400 [lbf]','N','goal','The maximum desired thrust.')
goal_of = EntryVar('OF','8.0','none','goal','The desired average OF ratio.')
goal_impulse = EntryVar('total_impulse','18 [kN*s]','N*s','goal','The desired total impulse.')
min_fuel_dp = EntryVar('min_fuel_dp','0.25','none','goal','The minimum fuel injector dp as a decimal percentage [0,1] of tank pressure.')
min_ox_dp = EntryVar('min_ox_dp','0.35','none','goal','The minimum fuel injector dp as a decimal percentage [0,1] of tank pressure.')
ox_to_fuel_time = EntryVar('ox_to_fuel_time','1.0','none','goal','The ratio of ox flow time to fuel flow time.')
Goal = Section('Goal', [max_thrust, goal_of, goal_impulse, min_fuel_dp, min_ox_dp, ox_to_fuel_time])

# Design
p_tanks = EntryVar('p_tanks','650 [psi]','Pa','design','The designed maximum operating pressure of the engine.')
ox_ull = EntryVar('ox_ullage','0.1','none','design','The decimal percentage of the ox tank that is gaseous at t=0.')
design_exp_ratio = EntryVar('exp_ratio','3.5','none','design','The designed nozzle expansion ratio.')
Design = Section('Design', [p_tanks, ox_ull, design_exp_ratio])

# Ox section
ox_Vtank = EntryVar('V_tank','6.63 [L]','m^3','initial_inputs.ox','The volume of the oxidizer tank.')
ox_Vliq = EntryVar('V_l','4.0 [L]','m^3','initial_inputs.ox','The volume of the liquid oxidizer in the tank at t=0.')
ox_tankID = EntryVar('tank_id','3.75 [in]','m','initial_inputs.ox','The internal diameter of the oxidizer tank.')
ox_hoffset = EntryVar('h_offset_tank','0 [in]','m','initial_inputs.ox','The distance from the bottom of the ox tank to the injector.')
ox_dflowline = EntryVar('d_flowline','0.25 [in]','m','initial_inputs.ox','The diameter of the flowline to the injector.')
ox_Ttank = EntryVar('T_tank','287.99043 [K]','K','initial_inputs.ox','The temperature of the oxidizer at t=0.')
Ox = Section('Oxidizer', [ox_Vtank, ox_Vliq, ox_tankID, ox_hoffset, ox_dflowline, ox_Ttank])

# OxPress section
oxpress_gas = GasVar('gas_properties','helium',structname='initial_inputs.ox_pressurant', description="Gas used as supercharging pressurant.")
oxpress_P = EntryVar('set_pressure','700 [psi]','Pa','initial_inputs.ox_pressurant','The regulated set pressure of the oxidizer pressurant source. ')
oxpress_Psource = EntryVar('storage_initial_pressure','4500 [psi]','Pa','initial_inputs.ox_pressurant','The pressure of the oxidizer pressurant source.')
oxpress_tankvol = EntryVar('tank_volume','3.5 [L]','m^3','initial_inputs.ox_pressurant','The volume of the ox pressurant source.')
oxpress_cda = EntryVar('flow_CdA','8 [mm^2]','m^2','initial_inputs.ox_pressurant','The CdA of the oxidizer pressurant regulator.')
oxpressvars = [oxpress_gas, oxpress_P, oxpress_Psource, oxpress_tankvol, oxpress_cda]
oxpress_active = ToggleVar('active',0,structname='initial_inputs.ox_pressurant',linkedvars=oxpressvars, description="Are you supercharging the oxidizer? Select for yes.")
OxPress = Section('Ox Pressurant', [oxpress_active] + oxpressvars)

# Fuel section
fuel_Vtank = EntryVar('V_tank','1.88 [L]','m^3','initial_inputs.fuel','The volume of the fuel tank.')
fuel_Vliq = EntryVar('V_l','0.66 [L]','m^3','initial_inputs.fuel','The volume of the liquid fuel in the tank at t=0.')
fuel_tankID = EntryVar('tank_id','3.75 [in]','m','initial_inputs.fuel','The internal diameter of the fuel tank.')
fuel_hoffset = EntryVar('h_offset_tank','24 [in]','m','initial_inputs.fuel','The distance from the bottom of the fuel tank to the injector.')
fuel_dflowline = EntryVar('d_flowline','0.25 [in]','m','initial_inputs.fuel','The diameter of the flowline to the injector.')
fuel_rhotank = EntryVar('rho','795 [kg*m^-3]','kg*m^-3','initial_inputs.fuel','The density of the fuel.')
Fuel = Section('Fuel', [fuel_Vtank, fuel_Vliq, fuel_tankID, fuel_hoffset, fuel_dflowline, fuel_rhotank])

# FuelPress section
fuelpress_gas = GasVar('gas_properties','nitrogen',structname='initial_inputs.fuel_pressurant', description="Gas used as supercharging pressurant.")
fuelpress_P = EntryVar('set_pressure','650 [psi]','Pa','initial_inputs.fuel_pressurant','The regulated set pressure of the fuel pressurant source. ')
fuelpress_Psource = EntryVar('storage_initial_pressure','4500 [psi]','Pa','initial_inputs.fuel_pressurant','The pressure of the fuel pressurant source.')
fuelpress_tankvol = EntryVar('tank_volume','0.0 [L]','m^3','initial_inputs.fuel_pressurant','The volume of the fuel pressurant source.')
fuelpress_cda = EntryVar('flow_CdA','8 [mm^2]','m^2','initial_inputs.fuel_pressurant','The CdA of the fuel pressurant regulator.')
fuelpressvars = [fuelpress_gas, fuelpress_P, fuelpress_Psource, fuelpress_tankvol, fuelpress_cda]
fuelpress_active = ToggleVar('active',1,structname='initial_inputs.fuel_pressurant',linkedvars=fuelpressvars, description="Are you supercharging the fuel? Select for yes.")
FuelPress = Section('Fuel Pressurant', [fuelpress_active] + fuelpressvars)

# Injector Section
ox_injarea = EntryVar('ox.injector_area','27.3 [mm^2]','m^2','initial_inputs','The area of the ox injector flowpaths.')
ox_cd = EntryVar('ox.Cd_injector', '1', 'unitless', 'initial_inputs', 'The discharge coefficient of the ox injector flowpaths.')
fuel_injarea = EntryVar('fuel.injector_area','2.1 [mm^2]','m^2','initial_inputs','The area of the fuel injector flowpaths.')
fuel_cd = EntryVar('fuel.Cd_injector', '1', 'unitless', 'initial_inputs', 'The discharge coefficient of the fuel injector flowpaths.')
dt_valve = EntryVar('dt_valve_open','0.01 [s]','s','initial_inputs','The time it takes for the primary valves to go from closed to fully open.')
Injector = Section('Injector', [ox_injarea,ox_cd, fuel_injarea,fuel_cd,dt_valve])

# Combustion Section
length_cc = EntryVar('length_cc', '4 [in]', 'm', 'initial_inputs', 'The length of the combustion chamber from injector face to start of nozzle.')
d_cc = EntryVar('d_cc', '3.75 [in]', 'm', 'initial_inputs', 'Internal diameter of the combustion chamber.')
nozz_eff = EntryVar('nozzle_efficiency', '0.95', 'unitless', 'initial_inputs', 'The nozzle efficiency (relative to an isentropic nozzle).')
nozz_corr = EntryVar('nozzle_correction_factor', '0.983', 'unitless', 'initial_inputs', 'The nozzle correction factor = 0.5*(1+cos(nozzle half angle)).')
cstar_eff = EntryVar('c_star_efficiency', '0.85', 'unitless', 'initial_inputs', 'The C* efficiency (relative to the ideal C*).')
dthroat = EntryVar('d_throat', '2.388e-2 [m]', 'm', 'initial_inputs', 'The nozzle throat diameter.')
exp_rat = EntryVar('exp_ratio', '3.5', 'unitless', 'initial_inputs', 'The nozzle expansion ratio.')
comb_data = MATVar('CombustionData','Combustion Data/CombustionData_T1_N2O.mat',structname='initial_inputs',description='.MAT file containing combustion data created using a RPA Nested Analysis for the chosen propellants.')
combvars = [length_cc, d_cc, nozz_eff, nozz_corr, cstar_eff, dthroat, exp_rat, comb_data]

Combustion = Section("Combustion", combvars)

# Simulation
T_amb = EntryVar('T_amb','280 [K]','K','initial_inputs','The ambient temperature.')
P_amb = EntryVar('p_amb','12.5 [psi]','Pa','initial_inputs','The ambient pressure.')
drymass = EntryVar('mass_dry_rocket', '50 [lb]', 'kg', 'initial_inputs', 'The mass of the rocket when empty of propellant, for flight simulation.')
plot_all = ToggleVar('plot_all',1,structname='options',description='Plot output in MATLAB for all PerformanceCode iterations? Select for yes.')
print_all = ToggleVar('print_all',1,structname='options',description='Print output for all PerformanceCode iterations? Select for yes.')
RAS_name = TXTVar('RAS_name', 'F_thrust_RASAERO.txt',structname='options',description='File name to which ENG file is saved.')
RAS_on = ToggleVar('RAS_on', 0, structname='options',linkedvars=[RAS_name],description="Create RAS .eng thrust curve from converged solution? Select for yes.")
Simulation = Section('Simulation', [T_amb, P_amb, drymass,plot_all,print_all, RAS_on, RAS_name])

''' Create result variables for DesignLiquid. '''
Fthrust = ResultVar('F_thrust', 'N', 'Generated thrust.')
p_cc = ResultVar('p_cc', 'Pa', 'Combustion chamber pressure.')
p_oxtank = ResultVar('p_oxtank', 'Pa','Ox tank pressure.')
p_oxpresstank = ResultVar('p_oxpresstank', 'Pa', 'Ox supercharging tank pressure.')
p_fueltank = ResultVar('p_fueltank','Pa', 'Fuel tank pressure.')
p_fuelpresstank = ResultVar('p_fuelpresstank','Pa', 'Fuel supercharging tank pressure.')
p_oxmanifold = ResultVar('p_oxmanifold','Pa','Oxidizer pressure in injector manifold.')
T_oxtank = ResultVar('T_oxtank', 'K', 'Temperature of ox tank.')
T_cc = ResultVar('T_cc','K','Temperature of the combustion chamber.')
area_core = ResultVar('area_core','m^2','Area of the fuel grain core (valid for hybrid only).')
gamma_ex = ResultVar('gamma_ex','none','Adiabatic constant of the exhaust gas.')
m_lox = ResultVar('m_lox','kg','Mass of liquid oxidizer left in the tank.')
m_gox = ResultVar('m_gox', 'kg', 'Mass of gaseous oxidizer left in the tank.')
m_fuel = ResultVar('m_fuel','kg','Mass of fuel left in the tank.')
p_crit = ResultVar('p_crit','Pa','Critical pressure of oxidizer.')
m_dot_ox_crit = ResultVar('m_dot_ox_crit','kg','Rate of ox flow per second, choked.')
M_e = ResultVar('M_e','none','Mach number of the exit flow.')
p_exit = ResultVar('p_exit','Pa','Pressure at nozzle exit.')
p_shock = ResultVar('p_shock','Pa','Pressure required to achieve normal shock at nozzle exit.')
time = ResultVar('time','s','Simulation time.')
m_ox = ResultVar('m_ox','kg','Total mass of oxidizer remaining.')
m_dot_ox = ResultVar('m_dot_ox','kg','Rate of ox flow per second.')
m_dot_fuel = ResultVar('m_dot_fuel','kg', 'Rate of fuel flow per second.')
OF = ResultVar('OF_i','none','OF ratio.')
m_dot_prop = ResultVar('m_dot_prop', 'kg', 'Rate of propellant flow per second out the nozzle.')
cstar = ResultVar('c_star_i','m','Characteristic exit velocity (per sec).')
c_f = ResultVar('c_f_i','none','Thrust coefficient.')
isp = ResultVar('Isp_i', 's', 'Specific impulse.')
ox_p_drop = ResultVar('ox_pressure_drop','Pa','Pressure drop between ox tank and injector.')
fuel_p_drop = ResultVar('fuel_pressure_drop','Pa','Pressure drop between fuel tank and injector.')
DesLiqResultVars = [Fthrust, p_cc, p_oxtank, p_oxpresstank, p_fueltank, p_fuelpresstank, p_oxmanifold,
                    T_oxtank, T_cc, area_core, gamma_ex, m_lox, m_gox, m_fuel, p_crit, m_dot_ox_crit,
                    M_e, p_exit, p_shock, time, m_ox, m_dot_ox, m_dot_fuel, OF, m_dot_prop, cstar, c_f,
                    isp, ox_p_drop, fuel_p_drop]

''' Create SimPage constructor arguments. '''
DesLiqSections = [Goal, Design, Ox, OxPress, Fuel, FuelPress, Injector, Combustion, Simulation]
DesLiqInputStructs = ["initial_inputs", "goal", "design","options"]
DesLiqPlotnames =  {'Thrust':{'unit': 'N', 'resultvars': [Fthrust]}, 
                    'Chamber Pressure':{'unit':'Pa','resultvars':[]},
                    'Tank Pressures':{'unit':'Pa', 'resultvars':[p_oxtank, p_fueltank]},
                    'Pressure Drop':{'unit':'Pa', 'resultvars':[ox_p_drop, fuel_p_drop]},
                    'Temperatures':{'unit':'Pa', 'resultvars':[]},
                    'Fuel':{'unit':'Pa', 'resultvars':[]},
                    'Oxidizer Mass Flux':{'unit':'Pa', 'resultvars':[]},
                    'Performance':{'unit':'Pa', 'resultvars':[]},
                    'Nozzle':{'unit':'Pa', 'resultvars':[]}
                   }

class DesignLiquidPage(SimPage):
    def __init__(self):
        super().__init__('DesignLiquid', DesLiqSections, DesLiqInputStructs)

    def prebuild(self, matlabeng):
        # Create Fuel and Ox Pressurant objects
        matlabeng.eval("initial_inputs.fuel_pressurant = Pressurant('fuel') ;", nargout = 0)
        matlabeng.eval("initial_inputs.ox_pressurant = Pressurant('oxidizer') ;", nargout = 0)

    def postbuild(self, matlabeng):
        matlabeng.eval("initial_inputs.comb_data = load(initial_inputs.CombustionData) ; initial_inputs.comb_data = initial_inputs.comb_data.CombData ;", nargout = 0)

    def run(self, stdout):
        input_struct_str = ','.join(self.inputstructs) # input struct
        
        self.matlabeng.eval( 'DesignLiquid(' + input_struct_str + ') ;' , nargout = 0, stdout = stdout)

    def plot(self, plotpane):
        ''' Plotting! Uses SimulateLiquidPage's defined version with different arguments. '''
        SimulateLiquidPage.plot(self, plotpane, is_design = True)

DesignLiquid = DesignLiquidPage()