import batman
import numpy as np
import matplotlib.pyplot as plt

R_Jupiter = 71492000
R_Sun = 695700000
R_star = 0.821 * R_Sun
Au = 149597870700

params = batman.TransitParams()
params.t0 = 0
params.per = 2.15222144
params.rp = 1.079 * R_Jupiter / R_star
params.a = 0.03138 * Au / R_star
params.inc = 84.73
params.ecc = 0.0; params.w = 0
params.limb_dark = 'quadratic'
params.u = [0.425, 0.179]

t = np.linspace(-.06, .06, 10000)
flux = batman.TransitModel(params, t).light_curve(params)

t_mins = t * 24 * 60

plt.figure(figsize=(7,4))
plt.plot(t_mins, flux, 'r')
plt.xlabel('Minutes from mid-transit')
plt.ylabel('Normalized stellar flux')
plt.title('WASP-2 Ab Transit light curve')
plt.grid(alpha=0.3)
plt.savefig("WASP-2_Ab_assignment1_taskF.png")
