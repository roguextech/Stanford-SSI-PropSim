
% Import test data from an excel sheet into the correct format for
% processing!

data = xlsread("Test Data/2020_03_08_Coldflow.xlsx");

open('fuel-cold-3-8-20_SDLog.mat');

%
%Format: 
% 1. Nitrous Line 
% 2. Nitrous HeatXger
% 3. Nitrogen 
% 4. Ox Tank
% 5. Ox/Manifold
% 6. LoadCell
% 7. Time (ms)
% 8. Last Command
%%
ValidTime = 3.558e5;

Time = data(ValidTime:end,7)/1000; % Seconds
Nitrous_Supply = data(ValidTime:end,1);
Nitrous_HeatXger = data(ValidTime:end,2); % Should Rename this but its ntrous line after Solenoid
Nitrogen_tank =data(ValidTime:end,3);
Ox_Tank = data(ValidTime:end,4);
Ox_Manifold = data(ValidTime:end,5);
LoadCell = data(ValidTime:end,6);
Last_Command = data(ValidTime:end,8);

figure()
title('Fuel Tank Pressure vs Time');
plot(Time,Nitrogen_tank)

figure()

hold on
plot(Time,Ox_Tank)
plot(Time,Nitrous_Supply)
plot(Time,Nitrous_HeatXger)
legend('Ox Tank','Nitrous Supply','Nitrous After Solenoid');
title('Ox Pressures vs Time');
xlabel('Time [s]');
ylabel('Pressure [s]');
hold off
%% Load Cell
Offset = mean(LoadCell);
n = 25
H = 1/n*ones(n,1);
Load_Filtered = filter(H,1,LoadCell);
figure()
plot(Time,Load_Filtered-Offset)
title('LoadCell');
xlabel('Time [s]');
ylabel('lbs');



