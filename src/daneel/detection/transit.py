import batman
import numpy as np
import matplotlib.pyplot as plt

r_Moon = 1737500
r_Earth = 6378000
r_Neptune = 24622000
r_Jupiter = 71492000
r_Sun = 695700000
Au = 149597870700


class TransitModel:
    def __init__(self, params_dict):
        self.params = batman.TransitParams()
        r_star = params_dict.get('r_star', 1) * r_Sun
        rp_unit = params_dict.get('rp_unit', r_Earth)

        self.params.t0 = params_dict.get('t0', 0.0)
        self.params.per = params_dict.get('per')
        self.params.rp = params_dict.get('rp') * rp_unit / r_star
        self.params.a = params_dict.get('a') * Au / r_star
        self.params.inc = params_dict.get('inc', 90.0)
        self.params.ecc = params_dict.get('ecc', 0.0)
        self.params.w = params_dict.get('w', 90.0)
        self.params.limb_dark = params_dict.get('limb_dark', 'quadratic')
        self.params.u = params_dict.get('u', [0.1, 0.3])

        self.t = np.linspace(-.06, .06, 10000)
        self.model = batman.TransitModel(self.params, self.t)

    def compute_light_curve(self):
        self.flux = self.model.light_curve(self.params)
        return self.flux

    def plot_light_curve(self, output_file='lightcurve.png', show=False):
        self.t_mins = self.t * 24 * 60

        if not hasattr(self, 'flux'):
            self.compute_light_curve()

        plt.figure(figsize=(7,4))
        plt.plot(self.t_mins, self.flux, 'r')
        plt.xlabel('Minutes from mid-transit')
        plt.ylabel('Normalized stellar flux')
        plt.title('WASP-2 Ab Transit light curve')
        plt.grid(alpha=0.3)
        plt.savefig(output_file)
        if show:
            plt.show()
        print(f"Light curve saved to {output_file}")

    def run(self, output_file='lightcurve.png'):

        self.compute_light_curve()
        self.plot_light_curve(output_file)
