% This function calculates the pressure loss in a pipe due to friction and
% altitude increase, and returns a positive value for pressure loss.
% It requires the fluid density rho, the velocity v, the pipe diameter d,
% the length l, the pipe roughness e, the viscosity mu, and the height
% change del_h. Along the way it calculates the Reynolds number r, the
% friction factor f, major losses, and height losses.

function [del_p] = pipe_flow(rho, v, d, l, e, mu, del_h)
    r = (rho.*v.*d)/mu;
    f = 1.325./(log(e/(3.7.*d)+5.74/(r.^0.9))).^2;
    major_losses = (f.*rho.*(v.^2).*l)/(2.*d);
    height_losses = rho.*9.8.*del_h;
    del_p = major_losses + height_losses;
end
    
    
