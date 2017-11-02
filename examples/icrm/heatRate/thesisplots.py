from beluga.visualization import BelugaPlot
from beluga.visualization.datasources import Dill, GPOPS
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from matplotlib2tikz import save as tikz_save

import functools as ft
import numpy as np
from math import sqrt, pi
import matplotlib as mpl

mpl.rcParams['axes.labelsize'] = 'x-large'
mpl.rcParams['legend.fontsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'x-large'
mpl.rcParams['ytick.labelsize'] = 'x-large'

output_dir = './plots/'
from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')
def save_pic(renderer, fig, p, suffix):
    fh = renderer._get_figure(fig)
    plt.tight_layout()
    tikz_save(f'{output_dir}/heatRate_{suffix}.tex', figureheight='\\figureheight', figurewidth='\\figurewidth')

def analytical_sol_xv(renderer, fig, p):

    save_pic(renderer,fig,p,'icrm_traj')

def analytical_sol_u(renderer, fig, p):

    save_pic(renderer,fig,p,'icrm_u')

plots = BelugaPlot('./data_fpa60.dill',default_sol=-1,default_step=-1)
mpbvp_ds = Dill('../../mpbvp/planarHypersonicWithHeatRate/data_1200.dill')
const_ds = Dill('./data_1200_ep4.dill')

plots.add_plot(colormap=cmx.gnuplot2).line_series('theta*180/3.14159','h/1000',step=1,skip=0,style={'lw':2.0}) \
                .xlabel('$\\theta$ [deg]').ylabel('$h$ [km]')\
                # .postprocess(ft.partial(save_pic, suffix='evol1_htheta'))

plots.add_plot(colormap=cmx.gnuplot2).line_series('t','gam*180/3.14159',step=1,skip=0,style={'lw':2.0}) \
                .xlabel('$t$ [s]').ylabel('$\\gamma$ [deg]')\
                # .postprocess(ft.partial(save_pic, suffix='evol1_fpa'))

rho = 'rho0*exp(-h/H)'
Cl  = '(1.5658*alfa + -0.0000)'
Cd  = '(1.6537*alfa**2 + 0.0612)'

D   = '(0.5*'+rho+'*v**2*'+Cd+'*Aref)'
L   = '(0.5*'+rho+'*v**2*'+Cl+'*Aref)'

plots.add_plot(colormap=cmx.viridis).line_series('t','k*sqrt(rho0*exp(-h/H)/rn)*v**3/10000',datasource=mpbvp_ds,step=-1,skip=2) \
                .xlabel('$t$ [s]').ylabel('$\\dot{q}$ [W/cm$^2$]') \
                .postprocess(ft.partial(save_pic, suffix='mpbvp_evol_qdot'))

plots.add_plot(colormap=cmx.viridis).line_series('v/1000','h/1000',datasource=mpbvp_ds,step=-1,skip=2) \
                .xlabel('$v$ [km/s]').ylabel('$h$ [km]') \
                .postprocess(ft.partial(save_pic, suffix='mpbvp_evol_hv'))


plots.add_plot()\
                .line('t','k*sqrt(rho0*exp(-h/H)/rn)*v**3/10000', datasource=mpbvp_ds, label='MPBVP', style={'lw':2.0}) \
                .line('t','k*sqrt(rho0*exp(-h/H)/rn)*v**3/10000', datasource=const_ds, label='ICRM', style={'lw':2.0}) \
                .xlabel('$t$ [s]').ylabel('$\\dot{q}$ [W/cm$^2$]') \
                .postprocess(ft.partial(save_pic, suffix='mpbvp_icrm_qdot'))

plots.add_plot()\
                .line('v/1000','h/1000', datasource=mpbvp_ds, label='MPBVP', style={'lw':2.0}) \
                .line('v/1000','h/1000', datasource=const_ds, label='ICRM', style={'lw':2.0}) \
                .xlabel('$v$ [km/s]').ylabel('$h$ [km]') \
                .postprocess(ft.partial(save_pic, suffix='mpbvp_icrm_hv'))


# plots.add_plot().line('theta*180/3.14','h/1000')                    \
#                 .xlabel('Downrange (km)').ylabel('h (km)')      \
#                 .title('Altitude vs. Downrange')
#
# plots.add_plot().line('t','alfa*180/3.14')                    \
#                 .xlabel('t (s)').ylabel('alfa (degrees)')      \
#                 .title('Angle of attack vs. Time')
#
#
# plots.add_plot().line('t','lamV')                    \
#                 .xlabel('t (s)').ylabel('lamV')      \
#                 .title('lamV vs. Time')

# rho = 'rho0*exp(-h/H)'
# Cl  = '(1.5658*alfa + -0.0000)'
# Cd  = '(1.6537*alfa**2 + 0.0612)'
#
# D   = '(0.5*'+rho+'*v**2*'+Cd+'*Aref)'
# L   = '(0.5*'+rho+'*v**2*'+Cl+'*Aref)'
#
# plots.add_plot().line('t','k*sqrt(rho0*exp(-h/H)/rn)*v**3/10000') \
#                 .xlabel('t (s)').ylabel('Heat-rate')      \
#                 .title('Heat-rate vs. Time')
# #
# # plots.add_plot().line('theta*re/1000','h/1000',label='Foo')       \
# #                 .line('theta*re/1000','h/1000',label='Bar',step=1,sol=5)   \
# #                 .xlabel('Downrange (km)')                   \
# #                 .ylabel('h (km)')                           \
# #                 .title('Altitude vs. Downrange')

plots.render()
