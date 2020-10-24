
%write function w/ inputs and outputs
%basic start: bernoulli -> gas gets cold as speeds up
%next add in compressible flow 
%then two-phase
%inputs: pressure and temp before orifice, area ratio of orifice. Output is
%temp at orifice
%
clear; clc; close all;
% convert stagnation to stagnant
% pressure drop of 1.8

P1 = 3000;
T1 = 300;
b1 = -6.71893;
b2 = 1.3596;
b3 = -1.3779;
b4 = -4.051;
Tcrit = 309.57; %K
Pcrit = 7251;   %kPa
syms T P
eqns = [P == exp((1/(T/Tcrit))*(b1*(1-(T/Tcrit)) + b2*(1-(T/Tcrit))^(3/2) + b3*(1-(T/Tcrit))^(5/2) + b4*(1-(T/Tcrit))^5))*Pcrit, P1/sqrt(T1) == P/sqrt(T)];
S = solve(eqns,[P T]);
Tstagnation = S.T;
P2 = S.P;

gamma = 1.4;
syms M;
eqn = 1 == (((gamma+1)/2)^((gamma+1)/(2*(gamma-1)))*(M/(1+(((gamma-1)/2)*M^2)^((gamma+1)/(2*(gamma-1))))));
M = solve(eqn)

T2 = Tstagnation * [1 + M^2 * (gamma-1)/2];




% function T = orifice_temp(P1, T1, Arat, v1)
% 
% end