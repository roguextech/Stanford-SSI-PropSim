# Liquid Rocket Engine Performance Code
## Stanford Student Space Initiative
## Palo Alto, California

----------------------------------------------
## ABOUT
This code is meant to simulate the performance of small liquid rocket engines.
Currently, the code is set to handle the properties of nitrous oxide as an
oxidizer. However, the properties of any fuel can be taken as input. 

* **Features:**
  * Two-phase nitrous oxide injector flow simulation using the Homogeneous 
   Equilibrium Model
  * Ability to import real combustion data varying with oxidizer to fuel 
   ratio and combustion chamber pressure.
  * Capability of simulating a self-pressurized oxidizer tank, an oxidizer
   tank with pressurant gas loaded in the ullage, or an oxidizer tank with an
   external pressurant gas supply tank with a regulator. 
  * Over fifteen plotting outputs allowing extensive insight into rocket 
   motor dynamics.
  * A simple Python-based graphic user interface for easy interaction.
   
* **Requirements:**
  * This code requires the MATLAB Optimization toolbox. Please make sure you have it installed before using!
  * If using the Python GUI, please see the **PYTHON GUI** section below about MATLAB engine requirements and 
requirements.txt location.

----------------------------------------------
## PYTHON GUI
**PropSim.pyw**  
  
This Python script loads a TKInter user interface that wraps the MATLAB foundations
of the performance code. This is done via the MATLAB-Python API provided by Mathworks,
which requires some basic set-up as described here: 
https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html

After checking that your version of Python works with the API for your version of MATLAB, run
the following lines in the MATLAB command line:  
```
	cd (fullfile(matlabroot,'extern','engines','python'))
	system('python setup.py install')
```    
The associated library and requirements.txt file for use is provided in `PythonLib/`. Open a command prompt in this folder and run  
``` 
	pip install -r requirements.txt 
```  
to ensure your package versions meet the requirements.  
  
Double-clicking this script will start the application.
  
----------------------------------------------
## MAIN SCRIPTS
**RunPerformanceCode.m**  
  
This script defines the characteristics of the liquid rocket engine to be
simulated and runs the simulation and output plotting. Options include
plotting outputs with test data in a specific format. This can run in a mode
that simulations only outflow of oxidizer (cold flow) or the full operation
of the rocket engine with combustion (hot fire). 
  
----------------------------------------------
## TEST CASES
Test cases are meant to easily verify that parts of the code are working for
development purposes. However, they may serve useful purposes.

### PlotN2OProperties.m
This script tests the generation of nitrous oxide oxidizer properties. It
also provides insight into the important properties of the chemical that
drive the rocket motor dynamics, such as the vapor pressure and its
dependence on temperature.

### TestCodeAccuracy.m
This script tests the numerical convergence of the simulation and can be used
to determine the numerical error as a function of time step. 

### TestNozzleCalc.m
This script tests the compressible quasi-1D flow calculator that is used
for nozzle calculations and injector gas flow calculations. 

### TestOxMassFlux.m
This script tests the calculation of two-phase nitrous oxide flow
calculation. The functions tested here are used for the prediction of
injector mass flow rate. 
  
----------------------------------------------
## GENERAL USAGE NOTES
* Scripts should always be run from the directory in which they are located.
* Combustion data is derived from the program RPA Lite v1.2. This program
  generates a text file which can be parsed with the provided function
  CombustionDataProcess.m
* Nitrous oxide properties are derived from data from the National Institute 
  of Standards and Technology's online chemical webbook.
* The "Test Data" directory is meant to hold test data to plot against
  performance code data. This data can be referenced by 
  RunHybridPerformance.m
* The RunHybridPerformance.m file can be used to store all information 
  about a rocket motor design.
  
----------------------------------------------
## DEVELOPMENT NOTES
* For ease of calculation, all units within the simulation are metric. This
  includes the following units: m, s, kg, K, mol, J, N. However, outputs or
  inputs may be defined in other convenient units. 
* Output variable recording is set up to be independent of the state
  calculation for run-time efficiency. 
  
----------------------------------------------
## THEORETICAL BASIS
* Tank Dynamics:
  * The liquid and gas within the oxidizer tank is assumed to be in thermal
   equilibrium. The van der Waal's equation is used to model the state of the
   gas and while not completely as accurate as empirical saturation state data,
   allows the calculation of non-saturated states. 
* Pressurant Gas:
  * Pressurant gas can be modeled as loaded into the ullage volume or supplied 
   from an external tank. In either case, all gas within the tank is assumed to
   be in thermal equilibrium with the nitrous oxide. Isentropic expansion is
   simulated in the external pressurant tank. 
* Injector Dynamics:
  * Two types of injector flow are modeled. While liquid remains in the tank, 
   two-phase flow is assumed, modeled using the Homogeneous Equilibrium Model.
   With only gas in the oxidizer tank, isentropic compressible quasi-1D flow 
   modelling is used. However, no frictional losses are modeled apart from a
   discharge coefficient factor for the injector orifices. 
* Combustion:
  * The combustion is modeled by predicting the exhaust properties within the
   combustion chamber. An efficiency factor, or c-star efficiency, is applied
   to the exhaust gas temperature. 
* Nozzle:
  * Quasi-1D isentropic flow is used to model the nozzle flow, including the
   cases of subsonic flow, supersonic flow, and normal shocks in the nozzle. 
   A nozzle exhaust thermal efficiency is applied to the exhaust energy. A
   correction factor accounting for the divergence factor of the nozzle is
   also applied. 
* Integration:
  * Euler's method is used for integration, using a constant time step.
  
----------------------------------------------
## TODO:
* Useability: 
  * Creation of a format for storing run data, so that runs can be stored and 
  graphed without rerunning the code every time and even more easily compared. 
  * Reformatting the data analysis function for user-friendliness. (Should come 
  after above). 

* Accuracy:
  * Upgrading of integration method. Removal of all of the Euler elements remaining
   in the integrator, so that it's fully handled by variable timestep ode15s
  * Implementing of drag in flow lines and cooling from orifices in mainline code. 
  * Upgrading of nitrous tank model to simulate pressure dip. Ongoing research effort. 
  Could possibly approximate by just preventing boil off for a certain time during burn.  
  * Replacing the Van der Waals equations of state with Peng-Robinson for greater accuracy 
  at supercritical temperatures. 

* Capability: 
  * Create tool for analyzing accelerometer data for combustion stability. 
  * Create GSE analysis tools. Given a launch time, how long do we have for tank load 
  before we reach supercritical? Input those settings into launch. 
  * Monte Carlo simulation. Be able to input a spread of input parameters and have the 
  code automatically provide the spread in a given output parameter. 
  * Add more propellant combinations to the database. 
  * Investigate differences between simulation and test data for
  supercharged oxidizer tank case
  
