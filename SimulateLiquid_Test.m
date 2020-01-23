%% Run Performance Code

addpath(fullfile(pwd, 'Supporting Functions'))

clear
close all

load('temp.mat')

options.t_final = 1;

%% Run Performance Code
PerformanceCode(inputs, mode, test_data, options);
