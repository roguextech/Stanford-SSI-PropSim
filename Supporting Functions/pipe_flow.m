% Calculates pressure loss (>0) due to friction and height.
% Inputs: fluid density rho, velocity u, diameter d,length l, 
% pipe roughness e, kinematic viscosity v, and height del_h.

function [del_p] = pipe_flow(rho, u, d, l, e, v, del_h)
    r = (u*d)/(v*10^-6); % v given * 10^-6 m^2/s
    f = 1.325/(log(e/(3.7*d)+5.74/(r^0.9)))^2;
    major_losses = (f*rho*(u^2)*l)/(2*d);
    height_losses = rho*9.8*del_h;
    del_p = major_losses + height_losses;
end

    
    
