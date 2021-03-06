import sys
from io import StringIO

from .EntryVar import EntryVar
from .ResultVar import ResultVar
from .ToggleVar import ToggleVar
from .MATVar import MATVar
from .GasVar import GasVar
from .Section import Section
from .SimPage import SimPage
from .SimulateLiquidPage import SimulateLiquidPage

''' Create input variables for SimulateHybrid and organize into Sections. '''
# Ox section
ox_Vtank = EntryVar('V_tank','20.0 [L]','m^3','inputs.ox','The volume of the oxidizer tank.')
ox_Vliq = EntryVar('V_l','18.0 [L]','m^3','inputs.ox','The volume of the liquid oxidizer in the tank at t=0.')
ox_tankID = EntryVar('tank_id','5.375 [in]','m','inputs.ox','The internal diameter of the oxidizer tank.')
ox_hoffset = EntryVar('h_offset_tank','0 [in]','m','inputs.ox','The distance from the bottom of the ox tank to the injector.')
ox_dflowline = EntryVar('d_flowline','0.5 [in]','m','inputs.ox','The diameter of the flowline to the injector.')
ox_Ttank = EntryVar('T_tank','289.1 [K]','K','inputs.ox','The temperature of the oxidizer at t=0.')
Ox = Section('Oxidizer', [ox_Vtank, ox_Vliq, ox_tankID, ox_hoffset, ox_dflowline, ox_Ttank])

# OxPress section
oxpress_gas = GasVar('gas_properties','helium',structname='inputs.ox_pressurant', description="Gas used as supercharging pressurant.")
oxpress_P = EntryVar('set_pressure','800 [psi]','Pa','inputs.ox_pressurant','The regulated set pressure of the oxidizer pressurant source. ')
oxpress_Psource = EntryVar('storage_initial_pressure','4500 [psi]','Pa','inputs.ox_pressurant','The pressure of the oxidizer pressurant source.')
oxpress_tankvol = EntryVar('tank_volume','3.5 [L]','m^3','inputs.ox_pressurant','The volume of the ox pressurant source.')
oxpress_cda = EntryVar('flow_CdA','.8 [mm^2]','m^2','inputs.ox_pressurant','The CdA of the oxidizer pressurant regulator.')
oxpressvars = [oxpress_gas, oxpress_P, oxpress_Psource, oxpress_tankvol, oxpress_cda]
oxpress_active = ToggleVar('active',0,structname='inputs.ox_pressurant',linkedvars=oxpressvars, description="Are you supercharging the oxidizer? Select for yes.")
OxPress = Section('Ox Pressurant', [oxpress_active] + oxpressvars)

# Fuel section
fuel_grainlength = EntryVar('grain_length','16.5 [in]','m','inputs.fuel','The length of the fuel grain.')
fuel_grainOD = EntryVar('grain_od','4.84 [in]','m','inputs.fuel','The outer diameter of the fuel grain.')
fuel_portrad = EntryVar('port_rad','1.2 [in]','m','inputs.fuel','The initial internal diameter of the fuel grain.')
fuel_n = EntryVar('n','0.67','none','inputs.fuel','Regression rate parameter, n.')
fuel_a = EntryVar('a','0.052 [mm*s^-1]','m*s^-1','inputs.fuel','Regression rate parameter, a.')
fuel_rho = EntryVar('rho','880 [kg*m^-3]','kg*m^-3','inputs.fuel','The density of the fuel grain.')
Fuel = Section('Fuel', [fuel_rho, fuel_grainlength, fuel_grainOD, fuel_portrad, fuel_n, fuel_a])

# Injector Section
injarea = EntryVar('injector_area','64.6 [mm^2]','m^2','inputs.ox','The area of the injector flowpaths.')
injcd = EntryVar('Cd_injector', '1', 'unitless', 'inputs.ox', 'The discharge coefficient of the injector flowpaths.')
dt_valve = EntryVar('dt_valve_open','0.1 [s]','s','inputs','The time it takes for the primary valve to go from closed to fully open.')
Injector = Section('Injector', [injarea, injcd, dt_valve])

# Combustion Section
length_cc = EntryVar('length_cc', '26 [in]', 'm', 'inputs', 'The length of the combustion chamber from injector face to start of nozzle.')
d_cc = EntryVar('d_cc', '5.375 [in]', 'm', 'inputs', 'Internal diameter of the combustion chamber.')
nozz_eff = EntryVar('nozzle_efficiency', '0.95', 'unitless', 'inputs', 'The nozzle efficiency (relative to an isentropic nozzle).')
nozz_corr = EntryVar('nozzle_correction_factor', '0.983', 'unitless', 'inputs', 'The nozzle correction factor = 0.5*(1+cos(nozzle half angle)).')
cstar_eff = EntryVar('c_star_efficiency', '0.87', 'unitless', 'inputs', 'The C* efficiency (relative to the ideal C*).')
dthroat = EntryVar('d_throat', '3.77e-2 [m]', 'm', 'inputs', 'The nozzle throat diameter.')
exp_rat = EntryVar('exp_ratio', '3.9', 'unitless', 'inputs', 'The nozzle expansion ratio.')
comb_data = MATVar('CombustionData','Combustion Data/CombustionData_80PR_20PP.mat',structname='inputs',description='.MAT file containing combustion data created using a RPA Nested Analysis for the chosen propellants.')
combvars = [length_cc, d_cc, nozz_eff, nozz_corr, cstar_eff, dthroat, exp_rat, comb_data]
comb_on = ToggleVar('combustion_on', 1, structname='mode',description='Is combustion occuring? Select if yes.',linkedvars=combvars)

Combustion = Section("Combustion", [comb_on]+combvars)

# Test Data
testfile = MATVar('test_data_file', '',structname='test_data',description='Data file to pull test data from.')
testoffset = EntryVar('t_offset', '0 [s]', 's', 'test_data', 'Time by which to offset the test data from the simulation data.')
test_plotting = ToggleVar('test_plots_on',0,structname='test_data',description='Import test data and plot against the simulation? Select for yes.', linkedvars=[testfile,testoffset])

TestData = Section('Test Data',[test_plotting, testfile, testoffset])

# Simulation
T_amb = EntryVar('T_amb','280 [K]','K','inputs','The ambient temperature.')
P_amb = EntryVar('p_amb','12.5 [psi]','Pa','inputs','The ambient pressure.')
t_final = EntryVar('t_final','60 [s]', 's', 'options', 'The end time of the simulation.')
delta_t = EntryVar('delta_t', '0.01 [s]', 's', 'options', 'Default time step used by the integrator.')
drymass = EntryVar('mass_dry_rocket', '70 [lb]', 'kg', 'inputs', 'The mass of the rocket when empty of propellant.')
flight_on = ToggleVar('flight_on', 0,structname='mode',linkedvars=[drymass],description='Simulate rocket flight? (Generates additional pressure head due to accelaration.')
plots_on = ToggleVar('print_on', 1, structname='options',linkedvars=[],description="Plot data in MATLAB pop-up? Select for yes.")
print_on = ToggleVar('plots_on', 1, structname='options',linkedvars=[],description="Print out summary info from run? Select for yes.")
RAS_on = ToggleVar('RAS_on', 0, structname='options',linkedvars=[],description="Create RAS .eng thrust curve from simulation? Select for yes.")
Simulation = Section('Simulation', [T_amb, P_amb, t_final, delta_t , flight_on, drymass, plots_on, print_on, RAS_on])

''' Create result variables for SimulateLiquid. '''
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
SimHybResultVars = [Fthrust, p_cc, p_oxtank, p_oxpresstank, p_fueltank, p_fuelpresstank, p_oxmanifold,
                    T_oxtank, T_cc, area_core, gamma_ex, m_lox, m_gox, m_fuel, p_crit, m_dot_ox_crit,
                    M_e, p_exit, p_shock, time, m_ox, m_dot_ox, m_dot_fuel, OF, m_dot_prop, cstar, c_f,
                    isp, ox_p_drop, fuel_p_drop]

''' Create SimPage constructor arguments. '''
SimHybSections = [Ox, OxPress, Fuel, Injector, Combustion, TestData, Simulation]
SimHybInputStructs = ["inputs", "mode", "test_data", "options"]
SimHybPlotnames =  {'Thrust':{'unit': 'N', 'resultvars': [Fthrust]}, 
                    'Chamber Pressure':{'unit':'Pa','resultvars':[]},
                    'Tank Pressures':{'unit':'Pa', 'resultvars':[p_oxtank, p_fueltank]},
                    'Pressure Drop':{'unit':'Pa', 'resultvars':[ox_p_drop, fuel_p_drop]},
                    'Temperatures':{'unit':'Pa', 'resultvars':[]},
                    'Fuel':{'unit':'Pa', 'resultvars':[]},
                    'Oxidizer Mass Flux':{'unit':'Pa', 'resultvars':[]},
                    'Performance':{'unit':'Pa', 'resultvars':[]},
                    'Nozzle':{'unit':'Pa', 'resultvars':[]}
                   }

class SimulateHybridPage(SimPage):
    def __init__(self):
        super().__init__('SimulateHybrid', SimHybSections, SimHybInputStructs)

    def prebuild(self, matlabeng):
        # Create Fuel and Ox Pressurant objects, load Combustion Data, and set options.output_on off (stops matlab from plotting)
        matlabeng.eval("mode.type = 'hybrid' ; ", nargout = 0)
        matlabeng.eval("inputs.ox_pressurant = Pressurant('oxidizer') ;", nargout = 0)

    def postbuild(self, matlabeng):
        if comb_on.get(): # if doing combustion, need to actually load the data into a struct
            matlabeng.eval("inputs.comb_data = load(inputs.CombustionData) ; inputs.comb_data = inputs.comb_data.CombData ;", nargout = 0)

    def run(self, stdout):
        input_struct_str = ','.join(self.inputstructs)
        
        self.matlabeng.eval( 'PerformanceCode(' + input_struct_str + ') ;' , nargout = 0, stdout = stdout, stderr = stdout)
    
    def plot(self, plotpane):
        ''' Plotting! Uses SimulateLiquidPage's defined version with different arguments. '''
        SimulateLiquidPage.plot(self, plotpane, is_liquid=False)

SimulateHybrid = SimulateHybridPage()