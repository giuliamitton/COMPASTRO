import batman
import numpy as np
import matplotlib.pyplot as plt


class TransitModel:
    def __init__(self, params_dict):
        self.params = batman.TransitParams()
        self.params.t0 = params_dict.get('t0', 0.0)
        self.params.per = params_dict.get('per')
        self.params.rp = params_dict.get('rp')
        self.params.a = params_dict.get('a')
        self.params.inc = params_dict.get('inc', 90.0)
        self.params.ecc = params_dict.get('ecc', 0.0)
        self.params.w = params_dict.get('w', 90.0)
        self.params.limb_dark = params_dict.get('limb_dark', 'quadratic')
        self.params.u = params_dict.get('u', [0.1, 0.3])

        self.t = np.linspace(-.06, .06, 10000)

    def compute_light_curves(self):    
        
        self.model_ref = batman.TransitModel(self.params, self.t)
        self.flux_ref = self.model_ref.light_curve(self.params)

        self.params.rp = self.params.rp/2

        self.model_half = batman.TransitModel(self.params, self.t)
        self.flux_half = self.model_half.light_curve(self.params)
        
        self.params.rp = self.params.rp * 4
        
        self.model_double = batman.TransitModel(self.params, self.t)
        self.flux_double = self.model_double.light_curve(self.params)

        return [self.flux_ref, self.flux_half, self.flux_double]

    def plot_light_curve(self, output_file='lightcurve.png', show=False):
        self.t_mins = self.t * 24 * 60

        if not hasattr(self, 'flux'):
            self.compute_light_curves()

        plt.figure(figsize=(7,4))
        plt.plot(self.t_mins, self.flux_ref, 'r', label='Reference Planet')
        plt.plot(self.t_mins, self.flux_half, 'g', label='Half-Radius Planet')
        plt.plot(self.t_mins, self.flux_double, 'b', label='Double-Radius Planet')
        plt.xlabel('Minutes from mid-transit')
        plt.ylabel('Normalized stellar flux')
        plt.title('WASP-10 b "Brothers" Transit light curves')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.savefig(output_file)
        if show:
            plt.show()
        print(f"Light curve saved to {output_file}")

    def run(self, output_file='lightcurve.png'):

        self.compute_light_curve()
        self.plot_light_curve(output_file)
